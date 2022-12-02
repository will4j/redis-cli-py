import urllib.parse
from urllib.parse import unquote
from urllib.parse import parse_qs
from urllib.parse import urlparse
from redis.connection import to_bool

import redis

URL_QUERY_ARGUMENT_PARSERS = {
    "db": int,
    "health_check_interval": int,
    "max_connections": int,
    "readonly": to_bool,
    "retry_on_error": list,
    "retry_on_timeout": to_bool,
    "socket_timeout": float,
    "socket_connect_timeout": float,
    "socket_keepalive": to_bool,
    "ssl": to_bool,
    "ssl_check_hostname": to_bool,
}


def parse_sentinel_url(url: urllib.parse.ParseResult):
    """
    redis+sentinel://[username:password@]host[:port][,host2[:port2],...][/service_name[/db]][?param1=value1[&param2=value=2&...]]
    :param url:
    :return:
    """
    def parse_host(host_str):
        if ':' in host_str:
            host, port = host_str.split(':', 1)
            port = int(port)
        else:
            host = host_str
            port = 26379
        return host, port

    kwargs = {}
    # query params
    for name, value in parse_qs(url.query).items():
        if value and len(value) > 0:
            value = unquote(value[0])
            parser = URL_QUERY_ARGUMENT_PARSERS.get(name)
            if parser:
                try:
                    kwargs[name] = parser(value)
                except (TypeError, ValueError):
                    raise ValueError(f"Invalid value for `{name}` in connection URL.")
            else:
                kwargs[name] = value

    # username and password
    if url.username:
        kwargs["username"] = unquote(url.username)
    if url.password:
        kwargs["password"] = unquote(url.password)

    # host and port
    netloc = unquote(url.netloc)
    if '@' in netloc:
        _, hostspec = netloc.split('@', 1)
    else:
        hostspec = netloc

    sentinels = [parse_host(s) for s in hostspec.split(',')]

    # path
    if url.path:
        path = unquote(url.path)
        path_parts = path.strip("/").split("/")
    else:
        path_parts = []

    # service_name
    if "service_name" not in kwargs and len(path_parts) > 0:
        kwargs["service_name"] = path_parts[0]
    # db
    if "db" not in kwargs and len(path_parts) > 1:
        kwargs["db"] = path_parts[1]

    return sentinels, kwargs


def init_from_url(url: str, **kwargs):
    """Init redis client from url.
    support scheme:
        [redis, rediss, unix, redis+sentinel]

    :param url: redis client url
    :param kwargs: additional redis client args
    :return:
    """
    url_parse = urlparse(url)
    if url_parse.scheme == "redis+sentinel":
        sentinels, connection_kwargs = parse_sentinel_url(url_parse)
        if "service_name" not in connection_kwargs:
            raise ValueError("Require param service_name for sentinel connection.")
        service_name = connection_kwargs.pop("service_name")
        sentinel = redis.Sentinel(sentinels, **connection_kwargs)
        RedisWrapper.init_from_sentinel(sentinel, service_name, **connection_kwargs)
    else:
        redis_instance = redis.from_url(url, **kwargs)
        RedisWrapper.init_from_redis(redis_instance)


class RedisWrapper:
    # borg pattern
    _shared_state = {}

    def __init__(self, redis_instance=None):
        self.__dict__ = self._shared_state
        if redis_instance is not None:
            self.redis = redis_instance

    @classmethod
    def get_redis(cls):
        new_instance = cls()
        if not hasattr(new_instance, "redis"):
            raise RuntimeError("Redis not inited, see redis_cli.init_from_* method.")
        return new_instance.redis

    @classmethod
    def init_from_redis(cls, redis_instance: redis.Redis):
        return cls(redis_instance=redis_instance)

    @classmethod
    def init_from_sentinel(cls, sentinel_instance: redis.Sentinel, service_name, **kwargs):
        readonly = kwargs.pop("readonly", False)
        if readonly:
            redis_instance = sentinel_instance.master_for(service_name, **kwargs)
        else:
            redis_instance = sentinel_instance.slave_for(service_name, **kwargs)

        return cls(redis_instance=redis_instance)
