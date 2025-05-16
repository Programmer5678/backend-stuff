from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import settings 

db_name = "to_do_list_db"
sql_connection_string_no_database = f"mysql+pymysql://ruz:{settings.mysql_pass}@localhost:3306/"
sql_connection_string = sql_connection_string_no_database + db_name
engine = create_engine(sql_connection_string, echo=True) #get the password from settings

SessionLocal = sessionmaker(engine)  #sessionmaker creates sessions that connect ton enigne 'engine'

#create session, yield it then get it back after done
def get_session():
    
    s = SessionLocal() 

    try: 
        yield s
    finally:
        s.close()