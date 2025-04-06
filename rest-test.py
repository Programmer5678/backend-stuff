import requests 
from fastapi import FastAPI
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

@app.get("/posts/{param}")
def blah(param : int):
    
    c.execute(f"select title, con from posts where id = {param};")
    ret = c.fetchall()
    
    if len( ret ):
        return { "id" : param, "title" : ret[0][0], "con" : ret[0][1] }
    return { "you say what?" : "what am i supposed to write here hehe" }

@app.post("/posts")
def f( x : Post ):
        
    c.execute(f"insert into posts( title , con ) values ( '{ x.title }', '{ x.con }' ) ;")
    mysql_run_and_pretty_print("""
use db;
select * from posts;
""")
    
    cnx.commit()
    
    c.execute(f"select id from posts order by id desc limit 1; ")
    
    return { "id" : c.fetchall()[0][0], "title" : x.title, "con" : x.con  }


@app.put("/posts/{id}")
def f2( x : Post, id : int):
    
	print(x, id )

	c.execute( f"select title, con from posts where id = {id};" )
	if len(c.fetchall()) :
		c.execute(f"update posts set title='{x.title}', con = '{x.con}' where id={id} ")
		cnx.commit()
  
		mysql_run_and_pretty_print("""
use db;
select * from posts;
""")
  
		return { "message" : "modified post!" } 
    
	return { "message" : "no post with such id..." } # should redirect!

@app.delete("/posts/{id}")
def f3(id: int):  
    c.execute("SELECT title, con FROM posts WHERE id = %s", (id,))  
    if len(c.fetchall()):  
        c.execute("DELETE FROM posts WHERE id = %s", (id,))  
        cnx.commit()

        mysql_run_and_pretty_print("""
        USE db;
        SELECT * FROM posts;
        """)

        return {"message": "deleted post!"}  

    return {"message": "no post with such id..."}  # should redirect?
