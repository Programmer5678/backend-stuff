import os
import time
from setup import setup
from sqlalchemy import text


session = setup()

query_res = session.execute( text("select name from bloglib order by id limit 150;") )

while ( next := query_res.fetchone() ):
    print(next[0])
    s = f"python main.py --read --name '{next[0]}'"
    os.system(s)

# for _ in range(100):
#     os.system("python main.py --read --name 'rotos initis'")