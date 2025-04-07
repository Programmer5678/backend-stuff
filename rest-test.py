import requests 

from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException , APIRouter, Depends
from fastapi.params import Body
from pydantic import BaseModel , EmailStr
import pandas as pd
from sqlalchemy import create_engine, text
from passlib.context import CryptContext

from jose import JWTError, jwt
from datetime import datetime, timedelta , timezone

from fastapi.security.oauth2 import OAuth2PasswordRequestForm,  OAuth2PasswordBearer

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated="auto" )

engine = create_engine("mysql+pymysql://ruz:p123@localhost:3306/db")
c = engine.connect() 

# c.execute("""create table users(id int primary key auto_increment, create_time timestamp default current_timestamp,
#           email varchar(100) not null , password varchar(100) not null)""")

# sql_query = pd.DataFrame(pd.read_sql_query('show create table users', c) )
# pd.set_option("display.max_rows", None)    # Show all rows
# pd.set_option("display.max_columns", None) # Show all columns
# pd.set_option("display.width", None)       # No fixed width
# pd.set_option("display.max_colwidth", None) # Don't truncate column contents
# print(sql_query)


app = FastAPI()

class Post( BaseModel ):
    title: str
    con: str

class UserCreate ( BaseModel ):
    email: EmailStr
    password: str
    
class UserLogin ( BaseModel ): #how to combine the schema with OAuthPasswordForm ???
    email: EmailStr
    password: str
    
class UserOut ( BaseModel ):
    id: int
    email: EmailStr
    
class Token ( BaseModel ):
    access_token: str
    token_type: str
    
class TokenAuth ( BaseModel ):
    id: int
    token: str
    
class Test ( BaseModel ):
    id : int

@app.get("/")
def root():
    return {"message" : "helloworld"}

@app.get("/posts")
def get_all_posts():
    
    query_result = c.execute(f"select * from posts")
    posts = [ { "id" : p[0], "title" : p[1], "con" : p[2] } for p in query_result.fetchall() ]
    
    return {"data" : posts}

@app.get("/posts/{param}")
def blah(param : int, response : Response):
    
    query_result = c.execute(f"select title, con from posts where id = {param};")
    ret = query_result.fetchall()
    
    if len( ret ):
        return { "id" : param, "title" : ret[0][0], "con" : ret[0][1] }
    
    raise HTTPException( status_code = status.HTTP_404_NOT_FOUND ,
        detail="no post with such id..."  )

@app.post("/posts")
def f( x : Post ):
        
    c.execute(f"insert into posts( title , con ) values ( '{ x.title }', '{ x.con }' ) ;")
#     mysql_run_and_pretty_print("""
# use db;
# select * from posts;
# """)
        
    return c.execute(f"select * from posts order by id desc limit 1; ").fetchall()[0]


@app.put("/posts/{id}")
def f2(x: Post, id: int, response: Response):
    # print(x, id)

    query_result = c.execute(f"SELECT title, con FROM posts WHERE id = {id};")
    if len(query_result.fetchall()):
        c.execute(f"UPDATE posts SET title='{x.title}', con = '{x.con}' WHERE id = {id}")

        # mysql_run_and_pretty_print("""
        # USE db;
        # SELECT * FROM posts;
        # """)

        return {"message": "modified post!"}

    raise HTTPException( status_code = status.HTTP_404_NOT_FOUND ,
        detail="no post with such id..."  )


@app.delete("/posts/{id}")
def f3(id: int):
        
    query_result = c.execute("SELECT title, con FROM posts WHERE id = %s", (id,))  
    if len(query_result.fetchall()):  
        c.execute("DELETE FROM posts WHERE id = %s", (id,))  

        # mysql_run_and_pretty_print("""
        # USE db;
        # SELECT * FROM posts;
        # """)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException( status_code = status.HTTP_404_NOT_FOUND ,
        detail="no post with such id..."  )

class UserOut ( BaseModel ):
    id: int
    email: EmailStr
    
# , response_model=UserOut
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def user_create(user : UserCreate):

    print(" hashing: ", user.password, "= ", pwd_context.hash(user.password))
    print(" hashing: ", user.password, "= ", pwd_context.hash(user.password))

    lastId = c.execute( text("insert into users(email, password) values( :email , :password )") , 
    {"email" : user.email , "password" : pwd_context.hash( user.password ) } ).lastrowid    
    # c.execute(f"insert into users(email, password) values('{user.email}' , '{user.password}' )" )
    
    # c.execute( text("""insert into users(email, password) values( :email, :password )""") , { "email" : "email@email.com", "password" : "password" } )
    # .inserted_primary_key[0]
    #      
    return c.execute( text("select * from users where id = :lastId"), {"lastId" : lastId} ).fetchone() 


router = APIRouter(  tags=["change tag in APIRouter to categorize docs"])

@router.get("/users/{id}",  response_model=UserOut)
def get_user(id : int):
    
    
    res = c.execute( text("select * from users where id = :id ") , {"id" : id} ).fetchone()
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"no user with id = {id}" )
    
    return res
    
@router.post("/login" , status_code=status.HTTP_201_CREATED)
def login( user : OAuth2PasswordRequestForm = Depends() ):
    
    query_res = c.execute( text("select password, id from users where email = :email") , {"email" : user.username} ).fetchone()
    
    if not query_res or not pwd_context.verify(user.password, query_res[0] ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")
    
    token = jwt.encode( {"id" : query_res[1], "exp" : ( datetime.now(timezone.utc) + timedelta(minutes=100) ) }
                              , "ds982983eodj3jwkldfldskldfsj89fdf8", algorithm="HS256" ) 
        
    return { "access_token" : token, "token_type" : "bearer" }
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')   

def verify_user( jwt_token : str = Depends(oauth2_scheme)  ):
    
    try: 
        data = jwt.decode(jwt_token, "ds982983eodj3jwkldfldskldfsj89fdf8", algorithms=["HS256"])
                
        expiary_date = datetime.fromtimestamp(data['exp'] , timezone.utc)
                
        print( datetime.now(timezone.utc) , expiary_date  , datetime.now(timezone.utc) > expiary_date )
        
        if datetime.now(timezone.utc) > expiary_date:
            raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="token expired. please log in again." ,
                                headers = {"WWW-Authenticate" : "Bearer"})
                
        return data['id']
    
    except JWTError:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid access token" ,
                            headers = {"WWW-Authenticate" : "Bearer"})

@router.get("/protected" )
def login( test : Test , token_id : int = Depends(verify_user) ):

    if not test.id == token_id:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="user id doesnt match access token",
                            headers = {"WWW-Authenticate" : "Bearer"} )

    return {"msg" : "secret message"}


    
    
    

    
# def verify_user( tokendata : TokenAuth ):
    
#     if not c.execute( text("select * from users where id = :id" ), tokendata.dict() ).fetchone() :
#         raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid user id" )
    
#     try: 
#         data = jwt.decode(tokendata.token, "ds982983eodj3jwkldfldskldfsj89fdf8", algorithms=["HS256"])
                
#         expiary_date = datetime.fromtimestamp(data['exp'] , timezone.utc)
                
#         print( datetime.now(timezone.utc) , expiary_date  , datetime.now(timezone.utc) > expiary_date )
        
#         if not data['id'] == tokendata.id:
#             raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="user id doesnt match access token" )
        
#         if datetime.now(timezone.utc) > expiary_date:
#             raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="token expired. please log in again." )
                
#         return True
    
#     except JWTError:
#         raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid access token" )
    
    
app.include_router(router)

 