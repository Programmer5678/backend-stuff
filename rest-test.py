import requests 
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import mysql.connector
from prettytable import PrettyTable 

cnx = mysql.connector.connect(user = 'ruz',
                               host = 'localhost',
                              password= 'p123',
                              database='db',
                              ssl_disabled=True)

c = cnx.cursor()


def pretty_print_mysql(out):
    
    print(out)

    if out.with_rows:  # Only fetch results for SELECT queries

        table = PrettyTable()

        table.field_names = [ i[0] for i in c.description ]

        for row in out:
            table.add_row(row)

        print( table )
    else:
        print("no output")

    print("")
    
def mysql_run_and_pretty_print(commands):
    for out in c.execute(commands , multi=True):
        pretty_print_mysql(out)

app = FastAPI()

class Post( BaseModel ):
    title: str
    con: str

@app.get("/")
def root():
    return {"message" : "helloworld"}

@app.get("/posts")
def get_all_posts():
    
    c.execute(f"select * from posts")
    posts = [ { "id" : p[0], "title" : p[1], "con" : p[2] } for p in c.fetchall() ]
    
    return {"data" : posts}

@app.get("/posts/{param}")
def blah(param : int, response : Response):
    
    c.execute(f"select title, con from posts where id = {param};")
    ret = c.fetchall()
    
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
    
    cnx.commit()
    
    c.execute(f"select id from posts order by id desc limit 1; ")
    
    return { "id" : c.fetchall()[0][0], "title" : x.title, "con" : x.con  }


@app.put("/posts/{id}")
def f2(x: Post, id: int, response: Response):
    # print(x, id)

    c.execute(f"SELECT title, con FROM posts WHERE id = {id};")
    if len(c.fetchall()):
        c.execute(f"UPDATE posts SET title='{x.title}', con = '{x.con}' WHERE id = {id}")
        cnx.commit()

        # mysql_run_and_pretty_print("""
        # USE db;
        # SELECT * FROM posts;
        # """)

        return {"message": "modified post!"}

    raise HTTPException( status_code = status.HTTP_404_NOT_FOUND ,
        detail="no post with such id..."  )


@app.delete("/posts/{id}")
def f3(id: int):
        
    c.execute("SELECT title, con FROM posts WHERE id = %s", (id,))  
    if len(c.fetchall()):  
        c.execute("DELETE FROM posts WHERE id = %s", (id,))  
        cnx.commit()

        # mysql_run_and_pretty_print("""
        # USE db;
        # SELECT * FROM posts;
        # """)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException( status_code = status.HTTP_404_NOT_FOUND ,
        detail="no post with such id..."  )
