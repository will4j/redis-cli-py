# Redis Python Client
Another redis python client :) redis-cli-py provides friendly access to redis (on both normal python apps and kubernetes apps), separating initialization and keys operation with borg pattern.  
You will have full features of official [redis-py](https://github.com/redis/redis-py), for the principle of this client is focusing on init, the interface you actually work with **IS** class *Redis* itself from redis-py, without wrapping, which will compatible with multiple versions of redis-py, including these in the future.

## Installation
### use pip
```bash
$ pip install redis-cli
```
### use git repository
```text
# this is requirements.txt
# git+https://gitee.com/will4j/redis-cli-py.git@main#egg=redis-cli
git+https://github.com/will4j/redis-cli-py.git@main#egg=redis-cli 
```
```bash
$ pip install -r requirements.txt
```

## Usage
### Basic example
```bash
>>> import redis_cli
>>> redis_cli.init_from_url("redis://localhost:6379")
>>>
>>> from redis_cli import get_redis
>>> get_redis().set('foo', 'bar')
True
>>> get_redis().get('foo')
b'bar'
```

### Initialization
**TIPS**: Both Redis and Sentinel actually use connectionpool internel, so do not bother with connectionpool.  
**NOTICE**: You can init redis_cli multiple times, but only one shared Redis instance will exists.
#### from existing redis instance
```python
import redis_cli
import redis

# from Redis instance
r = redis.Redis(host='localhost', port=6379, db=0)
redis_cli.init_from_redis(r)

# from Sentinel instance
s = redis.Sentinel([('localhost', 26379)], socket_timeout=0.1)
redis_cli.init_from_sentinel(s, 'mymaster')
```
#### from url
Scheme redis/rediss/unix will delegate to redis.from_url.  
Scheme redis+sentinel will be parsed, return master Redis (which can both read & write) or slave Redis (which is readonly),according to url param `readonly` (default false).
```python
import redis_cli

# from redis/rediss/unix url
redis_cli.init_from_url('redis://:password@localhost:6379/0')
redis_cli.init_from_url('rediss://localhost:6379/0')
redis_cli.init_from_url('unix://path/to/socket.sock?db=0')

# from sentinel url
redis_cli.init_from_url('redis-sentinel://username:password@host1:1,host2,host3:3/mymaster/0?readonly=true')
```

#### with env variables
This could be useful when deploy apps in kubernetes environment.  
**NOTICE**: `password` from url has the highest priority, then from env `REDISCLI_AUTH`. 
```bash
export REDISCLI_URL='redis-sentinel://host:26379/mymaster/0'
export REDISCLI_AUTH='complicated#pass'
```
```python
import redis_cli
# above env REDISCLI_URL and REDISCLI_AUTH will take over
redis_cli.init_from_url('redis://:password@localhost:6379/0')
```

### Operation
`get_redis()` returns shared Redis instance Based on how you init redis_cli, could be normal Redis, master Redis or slave Redis of sentinel.

```python
from redis_cli import get_redis

r = get_redis()
r.set('foo', 'bar')
r.get('foo')
r.delete('foo')
```

## References
1. https://github.com/redis/redis-py
1. https://github.com/exponea/redis-sentinel-url/blob/master/redis_sentinel_url.py
1. https://github.com/lettuce-io/lettuce-core/wiki/Redis-URI-and-connection-details
1. https://www.oreilly.com/library/view/python-cookbook/0596001673/ch05s23.html
1. https://huangzhw.github.io/2019/03/23/how-redis-py-sentinel-work
