
from tornado_json.requesthandlers import APIHandler
from tornado_json import schema
import json
from apps.db.models import *
import datetime
import uuid

class JobHandler(APIHandler):

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

        query_i = data['queries'][0]

        with psql_db.atomic():

            query_new = Queries.create(
                query_id=query_id,
                createdon = datetime.datetime.now(),
                query_type = query_type,
                result_location = '',
                status = 'RUNNING',
                result = '',
                error = ''
            )

            # get from celery
            taskid = uuid.uuid4()

            job_new = Jobs.create(
                job_id = taskid,
                query = query_new,
                query_name = query_i['name'],
                status = 'RUNNING',
                startedon = datetime.datetime.now()
            )

        self.success(data['fqid'])
