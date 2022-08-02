import redis
from typing import Any

class RedisWrapper:

    """

    A single parameter constructor accepting a source string representing the
    name of the configuration file containing relevant connection details.

    """

    def __init__(self, source: str):
        self.source = source
        self.redis = None
        
    """

    Connect(src) establishes a StrictRedis object to the file located at self.source.
    It expects self.source to be a text file consisting of 3 lines, each containing
    a host name, port number, and password. The order must be followed. For example:
    
        localhost
        5000
        password
    
    If parameter src is left as None, the self.source property from the __init__ method is used.
    If src is specified, self.source is assigned the value of src and then used.

    The StrictRedis object is stored in self.redis.

    """

    def connect(self, src=None) -> None:
        self.source = src if src != None else self.source
        data = []

        with open(self.source, 'r') as f:
            data = f.readlines()

        try:

            pwd = "" if len(data) != 3 else data[2].strip()
            self.redis = redis.StrictRedis(host=data[0].strip(), port=int(data[1].strip()), password=pwd, decode_responses=True)
            print("StrictRedis established.")
            print(data)
        except Exception as e:
            print(e)
            print(f"Error establishing RedisWrapper. Please check connection file specified at {self.source}")

    """
    
    IsConnected() returns true if self.redis has been established. And otherwise, false.

    """

    def isConnected(self) -> bool:
        return self.redis != None

    """
    
    Redis standard get / set
    
    """

    """
    
    RedisStdGet(key) returns the value associated with key-value pair, @param key. If the key is invalid,
    a None object will be returned.

    """

    def redisStdGet(self, key: Any) -> str:
        return self.redis.get(key)

    """
    
    RedisStdSet(key, value) explicitly sets a key-value pair in the Redis client object of @param key -> @param value.

    """
    
    def redisStdSet(self, key: Any, value: Any) -> bool:
        return self.redis.set(key, value)

    """
    
    RedisStdDelete(*keys) deletes an arbritrary number of keys from the Redis data store, given @param keys.
    It returns an integer representing the number of keys that were successfully deleted.

    """

    def redisStdDel(self, key: Any) -> int:
        return self.redis.delete(key)