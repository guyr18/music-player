from RedisWrapper import RedisWrapper
from TKClient import TKClient
from Resources import Resources
import os
 
# Clean sounds directory on startup.
dir = 'sounds/'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

wrapper = RedisWrapper("conf.txt")
wrapper.connect()
app = TKClient(title="PlayIt", geom="960x650")
Resources.REDIS_DB = wrapper
Resources.TK_CLIENT = app
app.mainloop()
