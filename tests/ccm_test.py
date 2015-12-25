from tornado.testing import AsyncHTTPTestCase
import apps.server.ccm as ccm

class CcmTest(AsyncHTTPTestCase):

    def get_app(self):
        return ccm.make_app()

    def test_status(self):
        response = self.fetch('/v1/status')
        self.assertEqual(response.code, 200)


