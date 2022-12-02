from urllib.parse import urlparse

import redis


class RedisWrapper:
    # borg pattern
    _shared_state = {}

    @classmethod
    def get_redis(cls):
        new_instance = cls()
        if not hasattr(new_instance, "redis"):
            raise RuntimeError("redis not inited.")
        return new_instance.redis

    def __init__(self, redis_instance: redis.Redis = None):
        self.__dict__ = self._shared_state
        if redis_instance is not None:
            self.redis = redis_instance

    @classmethod
    def init_from_url(cls, url: str, **kwargs):
        """

        :param url: redis client url, support scheme: [redis, rediss, unix, redis+sentinel, rediss+sentinel]
        :param kwargs: additional redis client args
        :return:
        """
        url_parse = urlparse(url)
        if url_parse.scheme in {"redis+sentinel", "rediss+sentinel"}:
            pass
        else:
            redis_instance = redis.from_url(url, **kwargs)
            cls(redis_instance=redis_instance)
