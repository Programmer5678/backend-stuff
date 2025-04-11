import os

from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException , APIRouter, Depends
from fastapi.params import Body
from pydantic import BaseModel , EmailStr, BaseSettings
import pandas as pd
from sqlalchemy import create_engine, text
from passlib.context import CryptContext

from jose import JWTError, jwt
from datetime import datetime, timedelta , timezone

from fastapi.security.oauth2 import OAuth2PasswordRequestForm,  OAuth2PasswordBearer

from starlette.middleware.cors import CORSMiddleware

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated="auto" )

# c.execute("""create table users(id int primary key auto_increment, create_time timestamp default current_timestamp,
#           email varchar(100) not null , password varchar(100) not null)""")

# sql_query = pd.DataFrame(pd.read_sql_query('show create table users', c) )
# pd.set_option("display.max_rows", None)    # Show all rows
# pd.set_option("display.max_columns", None) # Show all columns
# pd.set_option("display.width", None)       # No fixed width
# pd.set_option("display.max_colwidth", None) # Don't truncate column contents
# print(sql_query)

# logging.basicConfig( level=logging.INFO )
# logging.info()
    
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=[],
    allow_headers=[]
)

class Settings(BaseSettings):
    jwt_encrypt : str
    mysql_pass : str
    
    class Config:
        env_file = ".env"

settings = Settings()

engine = create_engine("mysql+pymysql://ruz:" +  settings.mysql_pass + "@localhost:3306/db"  )
c = engine.connect() 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')   

def get_user_id( jwt_token : str = Depends(oauth2_scheme) ) :
    
    return verify_user( jwt_token )


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
    
class LoginOut ( BaseModel ):
    access_token : str 
    token_type : str
    
class Token ( BaseModel ):
    access_token: str
    token_type: str
    
class TokenAuth ( BaseModel ):
    id: int
    token: str
    
class Testy ( BaseModel ):
    id : int

class ReturnPost ( BaseModel ):
    id : int
    title : str
    con : str
    owner_id : str
    

@app.get("/")
def root():
    return {"message" : "helloworld"}

@app.get("/posts")
def get_all_posts(limit : Optional[int] = None , offset : Optional[int] = None ,
                  search : str = ""):
        
        
    q = ("""select posts.id,title,con, owner_id, users.email as owner_email,
                             users.create_time as owner_create_time,
                             like_count
                             from posts 
                             left join users on owner_id = users.id 
                             left join like_count_table on posts.id = post_id 
                             """ 
    + """where posts.title like concat('%', :search ,'%') """ 
    + "order by posts.id " 
    + (" limit :limit " if limit else "" )
    #  + (" offset :offset ;" if offset else ";" )
    # + "offset 4;" 
    )
                              
    query_result = c.execute( text(q), { "limit" : limit, "offset": offset , "search" : search} )
    
    posts = [ { key : val for (key, val) in zip(list(query_result.keys()), p) } for p in query_result.fetchall() ]
        
    return {"data" : posts}

@app.get("/posts/{param}", response_model=ReturnPost)
def blah(param : int, response : Response):
    
    query_result = c.execute(f"select title, con, owner_id from posts where id = {param};")
    ret = query_result.fetchone()
    
    if len( ret ):
        return ReturnPost( id = param, title=ret[0], con=ret[1], owner_id = ret[2] )
    
    raise HTTPException( status_code = status.HTTP_404_NOT_FOUND ,
        detail="no post with such id..."  )

@app.post("/posts"   , response_model=ReturnPost    )
def f( x : Post , owner_id : int = Depends(get_user_id)):
            
    lastId = c.execute(text("insert into posts( title , con , owner_id) values ( :title , :con, :owner_id );")
              , { "title" : x.title, "con" : x.con, "owner_id" : owner_id } ).lastrowid
    
#     mysql_run_and_pretty_print("""
# use db;
# select * from posts;
# """)
    # return ReturnPost()
    return c.execute(f"select * from posts where id = {lastId} ").fetchone()


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
def f3(id: int, owner_id : int = Depends(get_user_id)):
    
        
    query_result = c.execute("SELECT title, con, owner_id  FROM posts WHERE id = %s", (id,)).fetchone()
    
    if query_result:  
        
        if owner_id == query_result[2]:
            c.execute(f"DELETE FROM posts WHERE id = {id}" )  
            
        else: 
            return Response(status_code=status.HTTP_403_FORBIDDEN )

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException( status_code = status.HTTP_404_NOT_FOUND ,
        detail="no post with such id..."  )
    

class UserOut ( BaseModel ):
    id: int
    email: EmailStr
    
# , response_model=UserOut
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def user_create(user : UserCreate):

    # print(" hashing: ", user.password, "= ", pwd_context.hash(user.password))
    # print(" hashing: ", user.password, "= ", pwd_context.hash(user.password))

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
    
@router.post("/login" , status_code=status.HTTP_201_CREATED, response_model=LoginOut)
def login( user : OAuth2PasswordRequestForm = Depends() ):
    
    query_res = c.execute( text("select password, id from users where email = :email") , {"email" : user.username} ).fetchone()
    
    if not query_res or not pwd_context.verify(user.password, query_res[0] ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")
    
    token = jwt.encode( {"id" : query_res[1], "exp" : ( datetime.now(timezone.utc) + timedelta(minutes=100) ) }
                              , settings.jwt_encrypt , algorithm="HS256" ) 
        
    return { "access_token" : token, "token_type" : "bearer" }


def verify_user( jwt_token ):
    
    try: 
        data = jwt.decode(jwt_token, settings.jwt_encrypt , algorithms=["HS256"])
                                
        return data['id']
    
    except JWTError as e:
        
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail= ("invalid access token: " + str(e)) ,
                            headers = {"WWW-Authenticate" : "Bearer"})

@router.get("/protected" )
def login( test : Testy , token_id : int = Depends( get_user_id ) ):

    if not test.id == token_id:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="user id doesnt match access token",
                            headers = {"WWW-Authenticate" : "Bearer"} )

    return {"msg" : "secret message"}


@router.post("/posts/{post_id}/like")
def like(post_id : int ,  user_id : int = Depends(get_user_id)  ):
    print(user_id , post_id)
    
    posts_query_res = c.execute(text("select * from posts where id = :post_id"), {"post_id" : post_id} ).fetchone()
    if not posts_query_res:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND  )


    likes_query_res = c.execute(text("select * from likes where user_id = :user_id and post_id = :post_id"),
              {"user_id" : user_id, "post_id" : post_id} ).fetchone()
    
    if likes_query_res:
        raise HTTPException( status_code=status.HTTP_409_CONFLICT , detail=f"""hello user with {user_id}, it seems you have already
                            liked post with id {post_id}""")
        
    c.execute(text("insert into likes (user_id , post_id) values ( :user_id , :post_id ) " ),
              {"user_id" : user_id, "post_id" : post_id} )
    
    # c.execute("insert into likes (user_id , post_id) values ( 68, 32 ) ")
    
    return {"message" : f"hello user with id {user_id}. successfuly liked post with id {post_id} " }
    
    
app.include_router(router)

 