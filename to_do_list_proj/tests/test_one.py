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
    
    
# test get all items by making sure each repsonse item is the same as appears on the db and
# response format is as expected 
def test_get_all_items(session, auth_client, created_user_id, created_items_ids):
    
    itemsFromDB = session.execute(
        text("select content from items where user_id = :user_id"), 
        {"user_id" : created_user_id }).mappings() # the items belongig to user according do database query
    
    response = auth_client.get("/main")
    
    for itemFromResponse in response.json()['items']: #loop through the items in the resposne
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
    
# test signing up with suername and password
def test_signup(client, session):
    username = "username hi"
    password = "mypassy"
    response = client.post("/signup" , json={"username" : username, "password" : password}) 
    
    query_res = session.execute(text("select password from users where username = :username"),
                                {"username" : username}).mappings().fetchall()
    
    assert len(query_res) == 1 #only one user with a given username!
    assert pwd_context.verify(password,  query_res[0]['password']) 
    # verify the password from users table of newly created user is correct
    assert SignUpReturn(**response.json()) #validate format
    assert response.status_code == status.HTTP_201_CREATED     
    
    
    