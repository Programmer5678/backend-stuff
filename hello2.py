import pandas as pd

from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://ruz:p123@localhost:3306/db")
c = engine.connect() 

c.execute(text("""update posts set id = 12 where id = 13; update posts set id = 15 where id = 19; """) )
c = engine.connect()

sql_query = pd.DataFrame(pd.read_sql_query('select * from posts', c) )
print(sql_query)

c.close()

#FIX THIS . the sexcute with autocommit is deprecated
