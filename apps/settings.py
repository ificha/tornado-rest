
# metastore
METASTORE_HOST="10.2.0.100"
METASTORE_PORT=9083

# postgres
POSTGRESQL_USER='postgres'
POSTGRESQL_PASSWD='postgres'
POSTGRESQL_HOST='192.168.99.100'

# celery
CELERY_BROKER_URL='redis://192.168.99.100:6379/0'
CELERY_RESULT_BACKEND='redis://192.168.99.100:6379/1'

# redis
DEFAULT_REDIS_URL = 'v2-001.owbwwo.0001.usw2.cache.amazonaws.com'
DEFAULT_CACHE_PAGE_SIZE = 20

# notidications
CCM_NOTIFICATION_ENDPOINT = 'http://localhost:8888/v1/notify'

# job server config
JOB_SERVER_CONTEXT = 'hli-jobs-ctx03'
JOB_SERVER_URL = 'http://localhost:8090/'

# query result location
QUERY_RESULTS_LOCATION = "hdfs://10.2.0.100/results/"

# celery tasks
RESILIENT_EXCEPTION_MAXTRY = 5
JOB_SERVER_PULL_INTERVAL_SEC = 3

# result cache
RESULT_CACHE_HOST='192.168.99.100'
RESULT_CACHE_PORT=6380

