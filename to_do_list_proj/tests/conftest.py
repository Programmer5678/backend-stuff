import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session
from base_for_tables import Base
from app import app
from engine_and_session import get_session
from tests.db_utils import create_db_if_not_exists, drop_and_recreate_db, testEngine
from tests.override_session import override_get_session
from fastapi.testclient import TestClient
from app import app
from handle_fastapi_auth import pwd_context
from tests.creds_utils import username_for_login_test, password_for_login_test


create_db_if_not_exists()
# Set dependency override
app.dependency_overrides[get_session] = override_get_session

@pytest.fixture
def session():
    drop_and_recreate_db()
    Base.metadata.create_all(testEngine)
    s = Session(bind=testEngine)
    try:
        yield s
    except:
        raise Exception("session create failed!")
    finally:
        s.close()
        testEngine.dispose()

@pytest.fixture
def client(session): 
    return TestClient(app)

#create a user in db for testing purposes
@pytest.fixture
def created_user_id(session):
    res = session.execute( text("insert into users(username , password) values(:username , :hash)"),
                    {"username" : username_for_login_test, 
                     "hash" : pwd_context.hash( password_for_login_test )} ) 
    session.commit()
    
    return res.lastrowid

@pytest.fixture
def created_items_ids(session, created_user_id):
    
    res = [ 
           session.execute( text("insert into items(content , user_id) values(:content , :user_id)"),
                    {"content" : "test content here! hooray!", 
                     "user_id" : created_user_id } ).lastrowid 
           for _ in range(10) ] #create 10 equivalent to-do-list items 
    
    session.commit()
    
    return res
    
    
@pytest.fixture
def login_response(created_user_id, client):
    return client.post("/login", data={"username" : username_for_login_test, 
                                           "password" : password_for_login_test } )
    
@pytest.fixture
def auth_client( login_response ):
    access_token = login_response.json()['access_token']
    auth_client = TestClient(app)
    auth_client.headers.update({"Authorization" : ("Bearer " + access_token ) })
    
    return auth_client