
from apps.db.models import Queries, Jobs, psql_db
from datetime import datetime
import json

def notification_event(task_id=None, state=None, retval=None):

    print("""
        celery task finish
        task id: %s
        state: %s
        retval: %s
        """ % (task_id, state, retval))

    update_db(retval, state, task_id)
    notify_external(retval, state, task_id)


def update_db(retval, state, task_id):

    job = Jobs.get(Jobs.job_id == task_id)
    query = Queries.get(Queries.query_id == job.query)
    job.status = state
    job.finishedon = datetime.now()
    query.status = state
    if state == 'SUCCESS':
        query.result = json.dumps(retval['result'])

    elif state == 'FAILURE':
        query.result = retval
    with psql_db.atomic():
        job.save()
        query.save()


def notify_external(retval, state, task_id):

    pass