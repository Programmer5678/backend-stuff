from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.params import Body
from sqlalchemy import text

from sqlalchemy.orm import Session
from settings import settings


from engine_and_session import get_session, engine
from base_for_tables import Base
from basemodels import NewItemRequest, getAllItemsResponse, Creds


app = FastAPI()
    
Base.metadata.create_all(engine)
    

@app.post("/old", status_code=status.HTTP_201_CREATED)
def old_new_item( payload : dict = Body(...), s : Session = Depends(get_session) ):
        
    if( "content" not in payload.keys() ): #if content not in payload, unproccessable
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="message invalid - no content passed...")
    
    print("password: ", settings.mysql_pass)
    
    s.execute(text("INSERT INTO testing (content) VALUES (:content)"), {"content": payload["content"]}) #insert the new item
    s.commit()
    
    return {"message" : "created!"}



@app.post("/", status_code=status.HTTP_201_CREATED)
def new_item( item : NewItemRequest , s : Session = Depends(get_session) ):
        
    print("password: ", settings.mysql_pass)
    
    
    s.execute(text("INSERT INTO testing (content) VALUES (:content)"), {"content": item.content}) #insert the new item
    s.commit()
    
    return {"message" : "created!"}

    
    
@app.get("/", 
         response_model=getAllItemsResponse 
         )
def get_all_items( s : Session = Depends(get_session) ):
        
    res = s.execute(text("select content from testing")).mappings().fetchall() #get all items in readable format
    
    return {"items" : res}



def check_username_not_exist(username : str, s : Session):
    return s.execute(text("select * from users where username = :username"), {"username" : username } ).fetchone()

@app.post("/signup", status_code=status.HTTP_201_CREATED )
def post_sign_up( creds : Creds,  s : Session = Depends(get_session)  ):
    
    
    
    if check_username_not_exist(creds.username , s):
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail="username already exists" )
    
    s.execute( text("insert into users(username, password) values(:username , :password) ") , creds.__dict__  )
    s.commit()
    
    return { "username" : creds.username }





    