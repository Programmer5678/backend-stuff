import pytest
from fastapi.testclient import TestClient
from fastapi import status
from jose import jwt
from rest_test import app, UserOut, settings, LoginOut

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
    
client = TestClient(app)

# def test_root() :
#     assert client.get('/').json().get('message') == 'helloworld'
    
# def test_get_all_posts() :
     
    
#     # print( client.get('/posts').json().get('data')  )

#     assert list(filter(
#         lambda x : x['id'] == 22 , 
#         client.get('/posts').json().get('data')  
#         ))[0]['title'] == 'my title 2 :)'
#     # assert client.get('/').json().get('message') == 'helloworld'
    
# @pytest.mark.parametrize( "email", [ ("email"), (5), ("neineleven"), (100), ("email@.co"), ("") ] )    
# def test_user_create_invalid_email(email):
    
#     res = client.post( "/users", json={"email" : email, "password" : "mypassword123"} )
    
#     assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
# @pytest.mark.parametrize( "email", [ ("newemail@email.com") , ("mamymail@email.com"), ("seewee@gmail.com") ] )    
# def test_user_create_successfully_and_valid_email(email) :
    
#     res = client.post( "/users", json={"email" : email, "password" : "mypassword123"} )
    
#     assert UserOut( **res.json() )
#     assert (res.status_code == status.HTTP_201_CREATED and res.json().get('email') == email )
    
@pytest.fixture( scope = "session")
def create_user():
    print("running create_user!")
    return ( client.post( "/users" , json= { "email" : "e@email.com" , "password" : "passy" } ) , "passy" )


def test_user_create( create_user ):
    
    res = create_user[0]
    
    assert UserOut( **res.json() )
    assert res.status_code == status.HTTP_201_CREATED 
    assert res.json().get("email") == "e@email.com"
    
    
def test_login( create_user ):
    
    email_from_create_user =  create_user[0].json().get("email")
    res=client.post("/login", data={"username" : email_from_create_user
                                , "password" : create_user[1] })
    
    print(res.json())
    
    id_from_token = jwt.decode( res.json()['access_token'] ,settings.jwt_encrypt , algorithms=["HS256"] )['id']
    email_from_token = client.get("/users/" + str(id_from_token) ).json()['email']
    
    assert LoginOut(**res.json()) 
    assert email_from_token == email_from_create_user 
    assert res.status_code == status.HTTP_201_CREATED
     

    
    
# def test_login():
#     res=client.post("/login", data={"username" : "newemail@email.com", "password" : "mypassword123"} )

#     client.get("/user")

#     id_from_token = jwt.decode( res.json()['access_token'] ,settings.jwt_encrypt , algorithms=["HS256"] )['id']
#     email_from_token = client.get("/users/" + str(id_from_token) ).json()['email']

#     # assert jwt.decode( res.json()['access_token'] ,settings.jwt_encrypt , algorithms=["HS256"] )['id']  ==  73  
#     assert email_from_token == "newemail@email.com"
#     assert res.status_code == status.HTTP_201_CREATED
#     assert res.json()['token_type'] == 'bearer'
     