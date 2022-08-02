from RedisWrapper import RedisWrapper
from json import dumps

wrapper = RedisWrapper()
wrapper.connect()
jsonValue = {
  "email": "admin@test.com",
  "password": "5f4dcc3b5aa765d61d8327deb882cf99",
  "favorites": None
}
jsonValue = dumps(jsonValue)
wrapper.redisStdSet("user:admin@test.com", jsonValue)
