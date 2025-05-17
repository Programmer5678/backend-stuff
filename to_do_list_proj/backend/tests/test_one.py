import pytest
from fastapi import status
from basemodels import *
from tests.creds_utils import username_for_login_test, password_for_login_test
from sqlalchemy import text
from random_string import random_string
from handle_fastapi_auth import pwd_context

def test_get_root(client):
    assert client.get("/").json()['message'] == 'blah'
    
# this tests if the login even works, we should get a jwt_token. doesnt check if the jwt_token actually works
def test_login_one(login_response):
    
    # print(login_response.json())
    
    assert login_response.status_code  == status.HTTP_200_OK
    assert LoginReturn(**login_response.json())
    
    
    
#pass in wrong credentials
@pytest.mark.parametrize( "username , password", [ (random_string(), random_string()),
                                                  ("usernaminami", "password"),
                                                  (username_for_login_test , random_string()),
                                                  (random_string(), password_for_login_test ),
                                                  (username_for_login_test.upper(), password_for_login_test),
                                                  (username_for_login_test, password_for_login_test.upper())] ,
                         ids=["case1", "case2", "case3", "case4", "case5", "case6"])
def test_wrong_creds_login(created_user_id, client, username, password):
    
    response = client.post("/login", data={"username" : username, 
                                           "password" : password } )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    
    
#pass in unproccessable creds - they dont fit the format. too short etc.
@pytest.mark.parametrize( "username , password", [ (random_string(), "siu"),
                                                  ("", ""),
                                                  ("uname" , "")] )
def test_unporccessable_login(created_user_id, client, username, password):
    
    response = client.post("/login", data={"username" : username, 
                                           "password" : password } )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
    
# test get all items by making sure each repsonse item is the same as appears on the db and
# response format is as expected 
def test_get_all_items(session, auth_client, created_user_id, created_items_ids):
    
    itemsFromDB = session.execute(
        text("select content from items where user_id = :user_id"), 
        {"user_id" : created_user_id }).mappings() # the items belongig to user according do database query
    
    response = auth_client.get("/main")
    
    db_items = session.execute(
    text("SELECT content FROM items WHERE user_id = :user_id"), 
    {"user_id": created_user_id}
).mappings().fetchall()

    response_items = response.json()["items"]

    assert len(db_items) == len(response_items)

    for itemFromDB, itemFromResponse in zip(db_items, response_items):#loop through the items in the resposne

        itemFromDB = itemsFromDB.fetchone() #last item from database
        assert itemFromResponse['content'] == itemFromDB['content'] # assert a match between the 2
    
    assert GetAllItemsResponse( **response.json() )
    assert response.status_code == status.HTTP_200_OK 

@pytest.mark.flaky(reruns=3) #because only probablistic guarentee
#post a new item and make sure there is one and only one item that matches exactly in the tablea
def test_post_new_item(session, auth_client, created_user_id, created_items_ids ):
    
    content = random_string()
    
    response = auth_client.post("/main", json={"content" : content})

    assert len(session.execute(text("select * from items where user_id = :user_id and content = :content")
    , {"user_id" : created_user_id, "content" : content }).fetchall()) == 1
    
    assert response.status_code == status.HTTP_201_CREATED
    assert NewItemReturn( **response.json() )
    
    
    
# test signing up with username and password
@pytest.mark.parametrize("username, password", [("username hi", "mypassy"),
                                                ("username jew", password_for_login_test)])
def test_signup(client, session, username, password):
    # username = "username hi"
    # password = "mypassy"
    response = client.post("/signup" , json={"username" : username, "password" : password}) 
    
    query_res = session.execute(text("select password from users where username = :username"),
                                {"username" : username}).mappings().fetchall()
    
    assert len(query_res) == 1 #only one user with a given username!
    assert pwd_context.verify(password,  query_res[0]['password']) 
    # verify the password from users table of newly created user is correct
    
    assert SignUpReturn(**response.json()) #validate format
    assert response.status_code == status.HTTP_201_CREATED     
    
    
#username and passwords that are too short - those dont match format
@pytest.mark.parametrize("username, password", [("", ""),
                                                ("username jew", ""),
                                                ("e", "e")])
def test_invalid_signup(client, session, username, password):
        
    response = client.post("/signup" , json={"username" : username, "password" : password}) 
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
#should get 409 conflict when i pass in username thats already in the db
def test_signup_username_already_exists(client, created_user_id):
    response = client.post("signup", json={"username" : username_for_login_test , "password" : random_string() } )
    
    assert response.status_code == status.HTTP_409_CONFLICT

    

    
    
    