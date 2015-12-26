from peewee import *
import datetime
from apps.settings import *
import os

psql_db = PostgresqlDatabase(
    os.environ.get('POSTGRESQL_DATABASE', 'ccm'),
    user = os.environ.get('POSTGRESQL_USER', POSTGRESQL_USER),
    password = os.environ.get('POSTGRESQL_PASSWD', POSTGRESQL_PASSWD),
    host = os.environ.get('POSTGRESQL_HOST', POSTGRESQL_HOST)
)

class Queries(Model):
    query_id = IntegerField(primary_key=True, index=True)
    createdon = DateTimeField(default=datetime.datetime.now)
    query_type = CharField(default='') # cohort; subcohort
    result_location = CharField(default='')
    status = CharField(default='')
    result = TextField(default='')
    error = TextField(default='')

    class Meta:
        database = psql_db

class Jobs(Model):
    job_id = UUIDField(primary_key=True, index=True)
    job_type = CharField(default='') # query; page_request
    job_params = CharField(default='') # for page_request -> cache_key
    query = ForeignKeyField(Queries, related_name='jobs')
    query_name = CharField(default='')
    status = CharField(default='')
    startedon = DateTimeField(default=datetime.datetime.now)
    finishedon = DateTimeField(default=datetime.datetime.min)

    class Meta:
        database = psql_db

def initialize():
    psql_db.connect()
    psql_db.create_tables([Queries, Jobs], safe=True)
