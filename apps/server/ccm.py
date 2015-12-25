
import tornado.ioloop
from job_handler import JobHandler
from status_handler import StatusHandler

def make_app():
    return tornado.web.Application([
        (r"/v1/status", StatusHandler),
        #(r"/v1/notify/?", NotificationHandler),
        (r"/v1/job/?", JobHandler),
        (r"/v1/job/([0-9a-f-]{36})", JobHandler),
    ], autoreload=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

