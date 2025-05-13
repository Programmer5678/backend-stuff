from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.params import Body
from sqlalchemy import text

from sqlalchemy.orm import Session
from settings import settings


from engine_and_session import get_session, engine
from base_for_tables import Base
from basemodels import NewItemRequest, getAllItemsResponse, Creds, LoginInput, LoginReturn, SignUpReturn
from validate_oauth_creds import validate_login_input
from handle_fastapi_auth import decode_jwt_token, ecncrypt_jwt_token, pwd_context, oauth2_scheme

from application_instance import app

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
    

@app.get("/")
def f():
    return {"message": "hi"}

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

def check_username_not_exist(username : str, s : Session):
    return s.execute(text("select * from users where username = :username"), {"username" : username } ).fetchone()

@app.post("/signup", status_code=status.HTTP_201_CREATED, response_model=SignUpReturn )
def post_sign_up( creds : Creds,  s : Session = Depends(get_session)  ):
    
    
    if check_username_not_exist(creds.username , s):
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail="username already exists" )
    
    s.execute( text("insert into users(username, password) values(:username , :password) ") , { "username" : creds.username, "password" : pwd_context.hash( creds.password ) }  )
    s.commit()
    
    return { "username" : creds.username }


@app.post("/login", response_model=LoginReturn)
def login(creds : LoginInput = Depends(validate_login_input),  s : Session = Depends(get_session) ):
    
    res = s.execute(text("select * from users where username = :username"), creds.__dict__ ).mappings().fetchone()
    
    
    if res and pwd_context.verify( creds.password , res['password'] ) :
        
        # token = jwt.encode( { "id" : res['id'] , "exp" : ( datetime.now(timezone.utc) + timedelta(minutes=100) )  },
        #           settings.jwt_secret
        #           ,algorithm="HS256" ) 
        
        token = ecncrypt_jwt_token( { "id" : res['id'] }, settings.jwt_secret, "HS256" )
        
        return {"access_token" : token , "token_type" : "bearer" }
    
    
    raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED )


       


@app.get("/protected_test")
def ppp( jwt_token : str = Depends(oauth2_scheme) ) :
    
    decode_jwt_token(jwt_token, settings.jwt_secret, "HS256" )
    
    return {"data" : "protected"}
    
    



