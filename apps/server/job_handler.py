
from tornado_json.requesthandlers import APIHandler
from tornado_json import schema
import json
from apps.db.models import *
import datetime
import uuid
from sql_validator import SqlValidator
from hive_metastore_adapter import HiveMetastoreAdapter
from apps.worker import tasks
from jsonschema import ValidationError
from apps.server.cache_manager import CacheManager


class JobHandler(APIHandler):

    @schema.validate(
        output_schema={
            "type": "object",
            "properties": {
                "fqid": {"type": "integer"},
                "status": {"type": "string"},
            }
        }
    )
    def get(self, fqid):
        query_id = int(fqid)

        try:
            query = Queries.get(Queries.query_id == query_id)
        except Exception, e:
            self.error(400, e.message)

        # get ?pages={"rdd1": { "page_size": 20, "page": 2 }}
        pages_dic = json.loads(self.get_argument('pages', None))
        pages = pages_dic.items()
        if pages is None:
            self.reply_error(405, 'pages is required')
            return

        # use only first now
        page = pages[0]
        rdd_name = page[0] # rdd_name is usefullnes at this moment (one query - one rdd)
        rdd_page = page[1]['page']
        rdd_page_size = page[1]['page_size']

        print('request query result: %s - %s - %s - %s' % (fqid, rdd_name, rdd_page, rdd_page_size))

        # get query params
        query_type = query.query_type
        result_location = query.result_location
        query_id = query.query_id
        status = query.status

         # job success -> get result
        if status == 'SUCCESS':

            # try to get data from cache
            cache_key = self._create_cache_key(query_id, query_type, rdd_page, rdd_page_size)
            print('cache_key: ' + cache_key)

            cache = CacheManager()

            if cache.is_key_exist(cache_key) is True:
                print('cache hit %s' % cache_key)
                return {
                    'data': cache.get_value(cache_key)
                }

            else:
                print('cache miss %s' % cache_key)

                # check is page is requesting
                try:
                    request_page_job = Jobs.get((Jobs.query == query.query_id) & (Jobs.job_params == cache_key) & (Jobs.job_type == 'page_request'))
                except Exception, e:
                    request_page_job = None

                # request job is running
                if request_page_job is not None:
                    if request_page_job.status not in ['SUCCESS', 'FAILURE']:
                        return {'ticket': request_page_job.job_id }
                    else:
                        return {'status': request_page_job.status}

                # request cache page

                spark_job_params = {
                    'cache': {
                      'result_location': result_location,
                      'cache_key': cache_key,
                      'skip': rdd_page_size * rdd_page,
                      'take': rdd_page_size,
                      'redis_connection': DEFAULT_REDIS_URL
                    }
                }

                # run spark job using celery
                async_result = tasks.submit_job.apply_async((spark_job_params, ))

                job_new = Jobs.create(
                    job_id = async_result.task_id,
                    job_type = 'page_request',
                    job_params = cache_key,
                    query = query,
                    query_name = '',
                    status = async_result.status,
                    startedon = datetime.datetime.now()
                )

                # this part is unclear!!!
                # how to notify client about result ready

                if async_result.status == 'SUCCESS':
                    data = async_result.result
                    return {'data': data}

                elif async_result.status == 'FAILURE':
                    raise Exception(message='\n'.join(async_result.result.args))

                else:
                    promise = {'ticket': async_result.task_id}
                    return {'promise': promise}

        # job failed -> error info
        elif status == "ERROR":
            self.reply_error(400, query.error)
            return

        # job still running -> return promise
        else:
            return {'status': 'still running'}



    @schema.validate(
        input_schema={
            "type": "object",
            "properties": {
                "fqid": {"type": "integer"},
                "query_type": {"type": "string"},
                "queries": {"type" : "array",
                    "items": {
                        "oneOf": [
                            {
                                "type": "object",
                                "properties":{
                                    "name": {"type": "string"},
                                    "sql": {"type": "string"}
                                },
                                "required": ["name", "sql"]
                            }
                        ]
                    }
                }
            },
            "required": ["fqid", "query_type", "queries"]
        }
    )
    def post(self):

        data = json.loads(self.request.body)

        query_id = data['fqid']
        query_type = data['query_type']

        queryExist = Queries.select().where(Queries.query_id == query_id)
        if queryExist:
            raise ValidationError(
                "Query id exists: %s" % query_id
            )

        query_i = data['queries'][0]


        query_name = query_i['name']
        query_sql = query_i['sql']

        # validate sql
        sqlValidator = SqlValidator(query_sql)
        if sqlValidator.is_valid() == False:
            self.error({'error': 'sql is not valid'})
            return

        tables = sqlValidator.get_tables()

        # validate hive metastor
        hiveMetastore = HiveMetastoreAdapter()
        if hiveMetastore.is_table_exist(tables[0]) == False:
            self.error({'error': 'one or more tables are not exist in hive metastore'})
            return

        table_meta = hiveMetastore.get_table_meta(tables[0])

        job_params = {
             "query": {
                "sql": query_sql,
                "tableName": table_meta['full_name'],
                "source_location": table_meta['location'],
                "result_location": self._get_result_location(query_type, query_id)
            },
            "cache": {
                "result_location": self._get_result_location(query_type, query_id),
                "cache_key": self._create_cache_key(query_id, query_type, 0, DEFAULT_CACHE_PAGE_SIZE),
                "skip": 0,
                "take": DEFAULT_CACHE_PAGE_SIZE,
                "redis_connection": DEFAULT_REDIS_URL
            }
        }
        async_result = tasks.submit_job.apply_async((job_params, ))
        # async_result.status; async_result.task_id;

        # save to db
        with psql_db.atomic():

            query_new = Queries.create(
                query_id=query_id,
                createdon = datetime.datetime.now(),
                query_type = query_type,
                result_location = self._get_result_location(query_type, query_id),
                status = async_result.status,
                result = '',
                error = ''
            )

            job_new = Jobs.create(
                job_id = async_result.task_id,
                job_type = 'query',
                query = query_new,
                query_name = query_name,
                status = async_result.status,
                startedon = datetime.datetime.now()
            )


        if async_result.status == 'SUCCESS':
            data = async_result.result
            return {'data': data}

        elif async_result.status == 'FAILURE':
            raise Exception(message='\n'.join(async_result.result.args))

        else:
            promise = {'ticket': async_result.task_id}
            return {'promise': promise}


    def _get_result_location(self, query_type, query_id):
        result_location = QUERY_RESULTS_LOCATION + "ds_" + query_type + "_" + str(query_id) + ".parquet"
        return result_location

    def _create_cache_key(self, fqid, query_type, page, page_size):
        cache_key = "ds_" + query_type + "_" + str(fqid) + "_" + str(page) + "_" + str(page_size)
        return cache_key