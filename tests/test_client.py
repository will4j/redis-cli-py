import pytest
from urllib.parse import urlparse

import redis_cli


def test_not_init():
    with pytest.raises(RuntimeError) as e:
        redis_cli.get_redis()
    exec_msg = e.value.args[0]
    assert exec_msg.startswith("Redis not inited,")


def test_url_redis():
    redis_cli.init_from_url("redis://127.0.0.1:6379")
    redis = redis_cli.get_redis()
    redis.delete("redis_test")
    assert redis.get("redis_test") is None
    assert redis.set("redis_test", "abc")
    assert redis.get("redis_test").decode() == "abc"


def test_parse_sentinel_url():
    url = "redis-sentinel://username:password@host1:1,host2,host3:3/mymaster/0?ssl=true&readonly=true&db=1"
    url_parse = urlparse(url)
    sentinels, connection_kwargs = redis_cli.client.parse_sentinel_url(url_parse)
    assert len(sentinels) == 3
    assert sentinels[1] == ('host2', 26379)
    assert sentinels[2] == ('host3', 3)
    assert connection_kwargs['service_name'] == "mymaster"
    assert connection_kwargs['ssl']
    assert connection_kwargs['readonly']
    assert connection_kwargs['db'] == 1
    assert connection_kwargs['username'] == "username"
    assert connection_kwargs['password'] == "password"
