import argparse
from sqlalchemy import text
from redis_setup import redis_setup
from setup import setup
import time

session = setup()
r = redis_setup()

parser = argparse.ArgumentParser(description="Hi guys. this is a help message")


parser.add_argument("--read", "-r", action="store_true" )
parser.add_argument("--name", "-n" )

args = parser.parse_args()

start_time=time.time()
        

def get_from_redis_or_db():
    redis_ret = r.get(args.name)
    
    if redis_ret:
        return redis_ret
    
    query_ret =  session.execute(text('select content from bloglib where name = :name'), args.__dict__  ).fetchone()
    
    if query_ret:
        return query_ret[0]
     
    return None

if args.read and args.name:
    
    res = get_from_redis_or_db()
    
    if res:
        print(f"worked. length: { len(res) }" )
        r.set(args.name, res)
    else:
        print("sad") 
    
end_time = time.time()

print("time it took: ", int(1000 * (end_time - start_time) ) )
    
r.shutdown()

session.close()