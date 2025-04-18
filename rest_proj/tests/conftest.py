import pytest
from fastapi.testclient import TestClient 
from rest_test import app, Post, ReturnPost, settings, get_session, Base
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import random

testEngine = create_engine("mysql+pymysql://ruz:" +  settings.mysql_pass + "@localhost:3306/db_test" 
                    #    , echo=True
                       )

TestSessionLocal = sessionmaker( testEngine )


@pytest.fixture(scope="session")
def session():
        
    s = TestSessionLocal()

    try: 
        yield s
    finally:
        s.close()
        
def override_get_session():
        
    s = TestSessionLocal()

    try: 
        yield s
    finally:
        s.close()


# Base.metadata.drop_all(testEngine)
Base.metadata.create_all(testEngine)
app.dependency_overrides[get_session] = override_get_session

@pytest.fixture
def anotherSession():
        
    s = TestSessionLocal()

    try: 
        yield s
    finally:
        s.close()

@pytest.fixture(scope="session")
def client(session):  
          
    return TestClient(app)


@pytest.fixture(scope="session")
def example_post_id(session):
    id = session.execute(text("insert into posts(title, con) values('my title 2 :)', 'contents') ")).lastrowid
    
    session.commit()
    
    return id

class CreateUser():
    
    def __init__( self, client, email , password):
        
        self.response = client.post( "/users" , json= { "email" : email , "password" : password } )
        self.email_from_request = email
        self.password_from_request = password
        
    def get_response(self):
        return self.response
        
    def get_email_from_response (self):
        return self.response.json().get("email")
    
    def get_id_from_response (self):
        return self.response.json().get("id")

    def get_email_from_request( self ):
        return self.email_from_request
    
    def get_password_from_request(self):
        return self.password_from_request
    

@pytest.fixture( scope = "session")
def create_users( client ):
    
    return [ CreateUser( client, "example" + str(str(random.randint(100, 10000000)) ) + "@email.com" , "password"),
             CreateUser( client, "example" + str(str(random.randint(100, 10000000)) ) + "@email.com" , "password") ]

@pytest.fixture( scope = "session")
def log_in_responses_users( client, create_users ):
        
    res = list(map( lambda create_user :  client.post("/login", data={"username" : create_user.get_email_from_response()
                                , "password" : create_user.get_password_from_request() })
              , create_users ) )
    
    # print("log_in_responses_users: ", res )
    
    return res


@pytest.fixture( scope = "session" )
def authorized_clients( log_in_responses_users):
            
    def log_in_response_to_authorized_client(log_in_response_user):
        access_token = log_in_response_user.json()['access_token']
        
        auth_cl = TestClient(app)
        auth_cl.headers.update({"Authorization" : ("Bearer " + access_token ) })
        
        return auth_cl
    
    return list(map( log_in_response_to_authorized_client , log_in_responses_users ))



@pytest.fixture( scope="session")
def create_posts(authorized_clients):
    
    
    authorized_client = authorized_clients[0]
    
    test_posts = [ Post(title = "my-title1", con = "contents1"), 
                  Post(title= "my-title2", con = "contents2"),
                  Post(title = "my-title3", con = "contents3"),
                  Post(title = "my-title4", con = "contents4") ]


    # authorized_client.post("/protected", json={"id" : 5} )
    authorized_client.post( "/posts", json={"title": "my-title1", "con" : "contents1"} )
    
    res_posts = list(map( 
                         lambda post : authorized_client.post( "/posts", json=post.__dict__ )
                        , test_posts
                        ))
        
    return { "body_request" : test_posts , "body_response" : res_posts }

@pytest.fixture
def create_post_for_delete(authorized_clients):
                    
    authorized_client = authorized_clients[0]
    return authorized_client.post("/posts", json={"title" : "soon to be deleted!", "con" : "soon to be deleted contents"})
         

@pytest.fixture
def create_post_for_update(authorized_clients):
                    
    authorized_client = authorized_clients[0]
    return authorized_client.post("/posts", json={"title" : "soon to be updated!", "con" : "soon to be updated contents"})