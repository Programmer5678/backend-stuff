import requests 
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

import pandas as pd
from sqlalchemy import create_engine


engine = create_engine("mysql+pymysql://ruz:p123@localhost:3306/db")
c = engine.connect() 

app = FastAPI()

class Post( BaseModel ):
    title: str
    con: str

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
    
    query_result = c.execute(f"select id from posts order by id desc limit 1; ")
    
    return { "id" : query_result.fetchall()[0][0], "title" : x.title, "con" : x.con  }


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
