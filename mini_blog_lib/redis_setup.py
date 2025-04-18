import subprocess as subp
import redis
import time

def redis_setup():

    subp.check_call( "redis-server redis.conf >/dev/null &  " , shell=True )
    
    start = time.time()
    
    r = None

    while True:
        
        try:  
            r = redis.Redis(port=6380)
            r.get("blah")            
            
        except:
                        
            time.sleep(0.01)
            
            if(time.time() - start) > 1:
                r.shutdown()
                raise redis.exceptions.TimeoutError("Timed out trying to connect to Redis.") 
            continue
        
        break
    
    return r