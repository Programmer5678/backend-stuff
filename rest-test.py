import requests 
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel , EmailStr

import pandas as pd
from sqlalchemy import create_engine

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
    
class UserOut ( BaseModel ):
    id: int
    email: EmailStr

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
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOut )
def user_create(user : UserCreate):
    
    c.execute(f"insert into users(email, password) values('{user.email}' , '{user.password}' )" )
    
    x = c.execute("select id, email from users where id = (select last_insert_id()) ").fetchall()[0]
    
    print(type(x))
    
    return x