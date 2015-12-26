
import time
import json
import requests.exceptions
from apps.settings import *
from celery import Celery
from celery.signals import task_postrun
from apps.server.notification import notification_event
from job_server_adapter import JobServerAdapter


# celery app
app = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

# events
@task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, task=None, args=None, kwargs=None, retval=None, state=None, **kwds):
    notification_event(task_id, state, retval)

if __name__ == '__main__':
    app.start()


@app.task(name='request_page', bind=True)
def request_page(self, job_params):

    print('submit_job: %s' % (job_params))

    adapter = JobServerAdapter()
    result = adapter.request_page_job(job_params)
    return pull_job_status(self, result['jobId'])


@app.task(name='submit_job', bind=True)
def submit_job(self, job_params):

    print('submit_job: %s' % (job_params))

    adapter = JobServerAdapter()
    result = adapter.query_job(job_params)
    return pull_job_status(self, result['jobId'])


def pull_job_status(celery_task, job_id):

    adapter = JobServerAdapter()
    resilientCount = 0
    while(True):

        print('pull_job_status - jobId: %s' % job_id)

        try:
            result = adapter.get_job_status(job_id)

            job_status = result['status']
            if job_status in [u'FINISHED']:

                # notify ccm
                notify_params = {
                    'task_id': celery_task.request.id,
                    'duration': result['duration'],
                    'status': job_status,
                    'result': result['result']
                }
                notify_params_json = json.dumps(notify_params)
                print('finish %s' % notify_params_json)
                return notify_params

            if job_status in [u'ERROR']:

                # notify ccm
                notify_params = {
                    'task_id': celery_task.request.id,
                    'duration': result['duration'],
                    'status': job_status,
                    'error': result['result']
                }
                notify_params_json = json.dumps(notify_params)
                print('finish %s' % notify_params_json)
                return notify_params

            time.sleep(JOB_SERVER_PULL_INTERVAL_SEC)

        except Exception, e:

            if resilientCount < RESILIENT_EXCEPTION_MAXTRY:
                resilientCount = resilientCount + 1
            else:
                raise
