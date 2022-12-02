import pytest

import redis_cli


def test_not_init():
    with pytest.raises(RuntimeError) as e:
        redis_cli.get_redis()
    exec_msg = e.value.args[0]
    assert exec_msg == "redis not inited."


def test_url_redis():
    redis_cli.init_from_url("redis://127.0.0.1:6379")
    redis = redis_cli.get_redis()
    redis.delete("redis_test")
    assert redis.get("redis_test") is None
    assert redis.set("redis_test", "abc")
    assert redis.get("redis_test").decode() == "abc"


