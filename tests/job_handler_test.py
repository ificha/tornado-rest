
from tornado.testing import AsyncHTTPTestCase
import apps.server.ccm as ccm
import json

def dumps(obj):
    return json.dumps(obj)

def loads(s):
    return json.loads(s.decode("utf-8"))

class CcTest(AsyncHTTPTestCase):

    def get_app(self):
        return ccm.make_app()


    # def test_job_post(self):
    #
    #     r = self.fetch(
    #         "/v1/job/",
    #         method="POST",
    #         body=dumps({
    #             "title": "Very Important Post-It Note",
    #             "body": "Equally important message",
    #             "index": 10
    #         })
    #     )
    #     self.assertEqual(r.code, 200)

