#The redis Queue
import os
import sys

if __name__ == "__main__":
    import inspect
    file_path = os.path.dirname(
        os.path.realpath(
            inspect.getfile(
                inspect.currentframe())))
    sys.path.insert(0, os.path.join(file_path, '../../'))

from database import redis as redis_cli
import configloader
import json
import tools
from tools.calculate import generate_uuid

class RedisQueue():
    def __init__(self,namespaced):
        self.c = configloader.config()
        self.r = redis_cli.newredis()
        self.namespaced = namespaced
        self.redis_queue_key_prefix = self.c.getkey("queue_prefix")+"."+self.namespaced
        self.redis_queue_key_main = self.redis_queue_key_prefix+".queuemain"

    def size(self):
        return self.r.llen(self.redis_queue_key_main)

    def empty(self):
        if self.r.llen(self.redis_queue_key_main) == 0:
            return True
        else:
            return False
        
    def clear(self):
        while not self.empty():
            key = str(self.r.rpop(self.redis_queue_key_main),encoding="utf-8")
            self.r.delete(self.redis_queue_key_prefix+"."+key)

    def push(self,value):
        key = generate_uuid()
        
        self.r.lpush(self.redis_queue_key_main,key)
        s = str(json.dumps(value))
        self.r.set(self.redis_queue_key_prefix+"."+key,s)
        
    
    def pop(self):
        try:
            key = str(self.r.rpop(self.redis_queue_key_main),encoding="utf-8")
        except:
            return None
        
        s = self.r.get(self.redis_queue_key_prefix+"."+key)
        self.r.delete(self.redis_queue_key_prefix+"."+key)
        out = json.loads(s)
        return out
    