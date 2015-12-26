
import tornado.ioloop
from job_handler import JobHandler
from status_handler import StatusHandler
from tornado_json.application import Application


def make_app():
    routes = [
        (r"/v1/status", StatusHandler),
        (r"/v1/job/?", JobHandler),
        (r"/v1/job/([0-9]+)", JobHandler),
    ]
    return Application(routes=routes, settings={})

if __name__ == "__main__":

    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

