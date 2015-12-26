import redis
from apps.settings import *

class CacheManager(object):

    def __init__(self):
        self.r = redis.StrictRedis(host=RESULT_CACHE_HOST, port=RESULT_CACHE_PORT)

    def is_key_exist(self, cache_key):
        return self.r.exists(cache_key)

    def get_value(self, cache_key):
        return self.r.get(cache_key)