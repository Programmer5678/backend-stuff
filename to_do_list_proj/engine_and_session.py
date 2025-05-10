from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import settings 

engine = create_engine(f"mysql+pymysql://ruz:{settings.mysql_pass}@localhost:3306/to_do_list_db", echo=True) #get the password from settings

SessionLocal = sessionmaker(engine)  #sessionmaker creates sessions that connect ton enigne 'engine'

#create session, yield it then get it back after done
def get_session():
    
    s = SessionLocal() 

    try: 
        yield s
    finally:
        s.close()