from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.params import Body
from sqlalchemy import text

from settings import settings
from sqlalchemy.orm import Session
from engine_and_session import get_session


app = FastAPI()


@app.post("/", status_code=status.HTTP_201_CREATED)
def new_item( payload : dict = Body(...), s : Session = Depends(get_session) ):
        
    if( "content" not in payload.keys() ): #if content not in payload, unproccessable
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="message invalid - no content passed...")
    
    print("password: ", settings.mysql_pass)
    
    s.execute(text("INSERT INTO testing (content) VALUES (:content)"), {"content": payload["content"]}) #insert the new item
    s.commit()
    
    return {"message" : "created!"}


@app.get("/")
def gets_item( payload : dict = Body(...) , s : Session = Depends(get_session) ):
    
    res = s.execute(text("select content from testing")).mappings().fetchall() #get all items in readable format
    
    return {"items" : res}
