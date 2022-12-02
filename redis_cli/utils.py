import redis

from redis_cli.client import RedisWrapper


def get_redis():
    return RedisWrapper.get_redis()


def init_from_url(url, **kwargs):
    return RedisWrapper.init_from_url(url, **kwargs)


def init_from_redis(redis_instance: redis.Redis):
    return RedisWrapper(redis_instance=redis_instance)
