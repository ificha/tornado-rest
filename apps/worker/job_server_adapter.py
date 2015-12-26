
import datetime
import requests
import json
from apps.settings import *
import uuid
import time


class JobServerException(BaseException):

    def __init__(self, msg):
        self.msg = msg


class JobServerAdapter(object):

    def __init__(self):
        self.test_count = 2

    def query_job(self, params):
        """
        :param params: spark_job_params
        :return: {'jobId': '', 'status': ''}
        """

        #test
        return {
            'jobId': uuid.uuid4(),
            'status': 'PENDING'
        }

        url = JOB_SERVER_URL + 'jobs?appName=' + JOB_SERVER_CONTEXT + '&classPath=hli.jobs.RequestPageJob'
        r = requests.post(url, data=json.dumps(params))
        r_json = r.json()

        if(r.ok):
            result = r_json['result']
            return result
        else:
            raise JobServerException(r.text)


    def request_page_job(self, params):
        """
        :param params:
        :return: {'jobId': '', 'status': ''}
        """

        #test
        return {
            'jobId': uuid.uuid4(),
            'status': 'PENDING'
        }

        url = JOB_SERVER_URL + 'jobs?appName=' + JOB_SERVER_CONTEXT + '&classPath=hli.jobs.QueryJob'
        r = requests.post(url, data=json.dumps(params))
        r_json = r.json()

        if(r.ok):
            result = r_json['result']
            return result
        else:
            raise JobServerException(r.text)


    def get_job_status(self, job_id):
        """
        :param job_id:
        :return: {'status': '', 'duration': '', 'result': ''}
        """

        # test
        if self.test_count > 0:
            self.test_count = self.test_count - 1
            return {'status': 'RUNNING'}
        else:
            self.test_count = 2
            return {
                'status': 'FINISHED',
                'duration': 1,
                'result': 'result value'
            }

        url = JOB_SERVER_URL + 'jobs/' + job_id
        r = requests.get(url)
        r_json = r.json()

        if(r.ok):
            return {
                'status': r_json['status'],
                'duration': r_json['duration'],
                'result': r_json['result'] if r_json.has_key('result') else 'no result'
            }
        else:
            raise JobServerException(r.text)
