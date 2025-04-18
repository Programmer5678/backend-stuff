import redis

r = redis.Redis(host='localhost', port=6379)

# print( r.set("France", "Paris") , r.set("Germany", "Berlin") , r.get("France"), r.get("Germany"),  r.get("Germanyy") ,
#       r.mset({"France" : "Tubes", "Germany" : "Boobs"}) )

# print(r.exists("France") , r.exists("Japan"))

if( r.exists("France") ):
    print("france: " + str(r.get("France")))
else:
    r.psetex("France", 10000 , "Paris")
    print("set france!")