from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.params import Body
from sqlalchemy import text

from sqlalchemy.orm import Session
from settings import settings


from engine_and_session import get_session, engine
from base_for_tables import Base
from basemodels import NewItemRequest, getAllItemsResponse
from handle_fastapi_auth import decode_jwt_token, oauth2_scheme
from application_instance import app

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


@app.get("/")
def g():
    return {"message": "blah"}  

@app.post("/old", status_code=status.HTTP_201_CREATED)
def old_new_item( payload : dict = Body(...), s : Session = Depends(get_session) ):
        
    if( "content" not in payload.keys() ): #if content not in payload, unproccessable
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="message invalid - no content passed...")
    
    print("password: ", settings.mysql_pass)
    
    s.execute(text("INSERT INTO testing (content) VALUES (:content)"), {"content": payload["content"]}) #insert the new item
    s.commit()
    
    return {"message" : "created!"}

@app.get("/main", 
         response_model=getAllItemsResponse 
         )
def get_all_items( s : Session = Depends(get_session), jwt_token : str = Depends(oauth2_scheme) ):
    
    decoded = decode_jwt_token(jwt_token, settings.jwt_secret, "HS256")
        
    res = s.execute(text("select content from items where user_id = :id"), decoded ).mappings().fetchall() #get all items in readable format
    
    return {"items" : res}

@app.post("/main", status_code=status.HTTP_201_CREATED)
def new_item( item : NewItemRequest , s : Session = Depends(get_session), jwt_token : str = Depends(oauth2_scheme)  ):
        
    # print("password: ", settings.mysql_pass)
    
    user_id = decode_jwt_token(jwt_token, settings.jwt_secret, "HS256")["id"]
    # print(user_id)
    
    s.execute(text("INSERT INTO items (content, user_id) VALUES (:content, :user_id)"), {"content": item.content, "user_id" : user_id}) #insert the new item
    s.commit()
    
    return {"message" : "created!"}






    