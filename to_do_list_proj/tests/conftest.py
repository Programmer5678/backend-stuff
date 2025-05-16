import pytest
from engine_and_session import sql_connection_string, sql_connection_string_no_database, db_name, get_session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from base_for_tables import Base
from app import app

test_db_name = db_name + "_test"
sql_connection_string_test = sql_connection_string + "_test"

#creates database test_db_name if doesnt exist already
def create_db_if_not_exists():
    engine = create_engine(sql_connection_string_no_database, echo=True )
    with engine.connect() as conn:
        
        try:
            conn.execute( text(f'create database if not exists {test_db_name}') )
        except:
            raise Exception("create database failed...")
        
    engine.dispose()

create_db_if_not_exists()
testEngine = create_engine(sql_connection_string_test, echo=True) 

def override_get_session():
        
    s = Session(bind=testEngine)

    try: 
        yield s
    finally:
        s.close()
        
app.dependency_overrides[get_session] = override_get_session

# drops and recreates database test_db_name
def drop_and_recreate_db():
    engine = create_engine(sql_connection_string_no_database, echo=True )
    with engine.connect() as conn:
        
        try:
            conn.execute( text(f'drop database {test_db_name}') )
        except:
            raise Exception("drop database failed...")
        
        try:
            conn.execute( text(f'create database {test_db_name}') )
        except:
            raise Exception("create database failed...")
    
    engine.dispose()

@pytest.fixture
def session():
    
    drop_and_recreate_db() #drop and recreate database every new session
    
    Base.metadata.create_all(testEngine) #create tables based on the metadata
    s = Session(bind=testEngine)
    
    try:
        yield s #yield the session to the pytest using it
    except:
        raise Exception("session create failed!")
    
    finally: #cleanup
        s.close()
        testEngine.dispose()
  
  
from fastapi.testclient import TestClient      
        
@pytest.fixture
def client(session):
    return TestClient(app)

  