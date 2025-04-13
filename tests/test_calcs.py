import pytest
from fastapi.testclient import TestClient
from fastapi import status
from jose import jwt
from rest_test import app, UserOut, settings, LoginOut, c, ReturnPost
from sqlalchemy import text
import random

# @pytest.fixture
# def my_fixture():
#     print("in my_fixture")
#     return 5

# def add(x, y):
#     return x + y

# @pytest.mark.parametrize ( "x, y, r" ,  [
#     ( 3, 4, 7 ),
#     ( 1, 9, 10),
#     ( 2, 2, 4)
# ] )
# def test_add(x, y, r):
#     print("SIUU")
#     assert x + y == r
    
    
# @pytest.mark.parametrize ( "x, y, r" , [
#     ( 3, 4, 7 ),
#     ( 1, 9, 10),
#     ( 2, 2, 4)
# ] )
# def test_mul(x, y, r):
#     assert x*y == r
    
# class Bank:

#     def __init__(self, amount = 0):
#         self.amount = amount
        
#     def deposit(self, n):
#         self.amount += n
        
#     def withdraw(self, n):
#         self.amount -= n
        
        
# def test_default_amount():
#     b = Bank()
#     assert b.amount == 0
    

# @pytest.mark.parametrize( "start, dep, expected", 
#                          [
#                              (20, 9, 29),
#                              (3, 0, 3),
#                              (100, 100, 200)
#                          ])
# def test_deposit_amount(start, dep, expected):
#     b = Bank(start)
#     b.deposit( dep )
    
#     assert b.amount == expected
    
    
    
# @pytest.mark.parametrize( "start, withdrawal, expected", 
#                          [
#                              (20, 9, 11),
#                              (3, 0, 11),
#                              (100, 100, 0)
#                          ])
# def test_withdraw_amount(start, withdrawal, expected):
#     b = Bank(start)
#     b.withdraw( withdrawal )
    
#     assert b.amount == expected
    
    
# def test_example( my_fixture ):
#     print("in test_example")
#     assert my_fixture == 5
    
# class Exy(Exception):
#     pass
    
# def test_expecting_error() :
    
#     with pytest.raises(Exy):
#         raise Exy("tsup")        

# def test_root() :
#     assert client.get('/').json().get('message') == 'helloworld'
    
def test_get_all_posts(client) :
     
    
    # print( client.get('/posts').json().get('data')  )

    assert list(filter(
        lambda x : x['id'] == 22 , 
        client.get('/posts').json().get('data')  
        ))[0]['title'] == 'my title 2 :)'
    # assert client.get('/').json().get('message') == 'helloworld'
    
# @pytest.mark.parametrize( "email", [ ("email"), (5), ("neineleven"), (100), ("email@.co"), ("") ] )    
# def test_user_create_invalid_email(email):
    
#     res = client.post( "/users", json={"email" : email, "password" : "mypassword123"} )
    
#     assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
# @pytest.mark.parametrize( "email", [ ("newemail@email.com") , ("mamymail@email.com"), ("seewee@gmail.com") ] )    
# def test_user_create_successfully_and_valid_email(email) :
    
#     res = client.post( "/users", json={"email" : email, "password" : "mypassword123"} )
    
#     assert UserOut( **res.json() )
#     assert (res.status_code == status.HTTP_201_CREATED and res.json().get('email') == email )

def test_user_create( create_users ):
    
    for create_user in create_users:
        res = create_user.get_response()
        
        assert UserOut( **res.json() )
        assert res.status_code == status.HTTP_201_CREATED 
        assert create_user.get_email_from_request() == create_user.get_email_from_response()
        
    
    
def test_login( client, create_users, log_in_responses_users):
    
    for (create_user, log_in_response_user) in zip(create_users, log_in_responses_users) :
    
        email_from_create_user =  create_user.get_email_from_response()
                    
        id_from_token = jwt.decode( log_in_response_user.json()['access_token'] ,settings.jwt_encrypt , algorithms=["HS256"] )['id']
        email_from_token = client.get("/users/" + str(id_from_token) ).json()['email']
        
        assert LoginOut(**log_in_response_user.json()) 
        assert email_from_token == email_from_create_user 
        assert log_in_response_user.status_code == status.HTTP_201_CREATED


FROM_CREATE_USER = 1057
@pytest.mark.parametrize( "username, password" , [ ("fake-user1" , FROM_CREATE_USER ), ("fake-user2", "fake-password2"),
                                                 ("fake-user2", FROM_CREATE_USER ) ] )
def test_login_fail(client, create_users, username, password):
    
    for create_user in create_users:
    
        if username == FROM_CREATE_USER:
            username=create_user.get_email_from_response()
            
        if password == FROM_CREATE_USER:
            password=create_user.get_password_from_request()
        
        res=client.post( "/login", data={"username" : username , "password" : password})
        
        # print(res)
        
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
        assert res.json()['detail'] == "invalid credentials"

def test_protected(create_users, authorized_clients):
    
    for (create_user, authorized_client) in zip(create_users, authorized_clients) :
    
        id = create_user.get_id_from_response() 
        
        res = authorized_client.post("/protected", json={"id" : id}) 
        
        # print(res.status_code, res.json())

        assert res.json()['msg'] == "secret message"


# @pytest.mark.parametrize("title, con" ,
#     [ ("this is a title", "this is contents") 
#      , ("this is a title 2", "this is contents 2") 
#      , ("this is a title 3", "this is contents 3") 
#      , ("this is a title 4", "this is contents 4") 
#      , ("this is a title 5", "this is contents 5") 
#      ])
# def test_post(authorized_client, title, con):
#     res = authorized_client.post( "/posts", json={"title" : title, "con" : con } )
    
#     post_details_from_resposne = ReturnPost( **res.json() )
#     post_details_from_sql = ReturnPost( **c.execute(text("select * from posts where id = :id"), 
#                                                     {"id" : post_details_from_resposne.id}).fetchone()  )
#     assert post_details_from_resposne == post_details_from_sql

# def test_get_post(client, ):
#     client.get("/post/")




def test_create_post(create_posts):
    
    for (req, res) in zip(create_posts["body_request"] , create_posts["body_response"]):
        
        post_details_from_resposne = ReturnPost( **res.json() )
        
        assert req.title == post_details_from_resposne.title
        assert req.con == post_details_from_resposne.con 
        
        post_details_from_sql = ReturnPost( **c.execute(text("select * from posts where id = :id"), 
                                                    {"id" : post_details_from_resposne.id}).fetchone()  )
        
        assert res.status_code == status.HTTP_201_CREATED
        assert post_details_from_resposne == post_details_from_sql
        
        
def test_get_post(client, create_posts):
    
    for res_create_post in create_posts['body_response']:
        
        res_get_post = client.get("/posts/" + str( res_create_post.json()['id'] ) )
        
        assert res_get_post.status_code == 200
        assert res_create_post.json() == res_get_post.json() 
        
        
def test_unauthorized_create_post(client):
    res = client.post("/posts", json={"title" : "tities", "con" : "why tities dont grow past 20(and how to fix it!)"})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    assert res.json()['detail'] == "Not authenticated"
    
def test_unauthorized_delete_post(client):
    res = client.delete("/posts/102320")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    assert res.json()['detail'] == "Not authenticated"
        
    
def test_delete_post(authorized_clients, create_post_for_delete):
        
    print(authorized_clients)
    authorized_client = authorized_clients[0]
    
    id = create_post_for_delete.json()['id']
    res = authorized_client.delete( f"/posts/{id}" )
    assert res.status_code == status.HTTP_204_NO_CONTENT    
    assert c.execute(text("select * from posts where id = :id"), {"id" : id}).fetchone() == None
    
def test_delete_post_not_exist(authorized_clients):
    
    authorized_client = authorized_clients[0]
    
    res = authorized_client.delete( "/posts/" + str(random.randint(1000, 10000)) )
    assert res.status_code == status.HTTP_404_NOT_FOUND
    
def test_delete_other_user_post(authorized_clients, create_posts ):
    other_user_client = authorized_clients[1]
    post = create_posts["body_response"][0]
    
    res = other_user_client.delete(f"/posts/{post.json()['id']}")
        
    assert res.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.parametrize( "title, con", [ ("title juan", "con juan"),
                                         ("title dva", "con juan"), 
                                         ("title juan", "con dva") ] )
def test_update_post(authorized_clients, create_post_for_update, title, con):
        
    authorized_client = authorized_clients[0]
    
    id = create_post_for_update.json()['id']
    res = authorized_client.put( f"/posts/{id}", json={"title": title, "con" : con} )
    assert res.status_code == status.HTTP_200_OK
    assert res.json()['message'] == 'modified post!'
    assert c.execute(text("select title, con from posts where id = :id"), {"id" : id}).fetchone() == (title, con)
    
    
@pytest.mark.parametrize( "title, con", [ ("title juan", "con juan"),
                                         ("title dva", "con juan"), 
                                         ("title juan", "con dva") ] )
def test_update_post_other_user(authorized_clients, create_post_for_update, title, con):
        
    other_user_client = authorized_clients[1]
    
    id = create_post_for_update.json()['id']
    res = other_user_client.put( f"/posts/{id}", json={"title": title, "con" : con} )
    assert res.status_code == status.HTTP_403_FORBIDDEN