from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy import text

from sqlalchemy.orm import Session
from settings import settings

from engine_and_session import get_session, engine
from basemodels import Creds, LoginInput, LoginReturn, SignUpReturn
from validate_oauth_creds import validate_login_input
from handle_fastapi_auth import decode_jwt_token, ecncrypt_jwt_token, pwd_context, oauth2_scheme


router_auth = APIRouter(  tags=["change tag in APIRouter to categorize docs"])

def check_username_not_exist(username : str, s : Session):
    return s.execute(text("select * from users where binary username = :username"), {"username" : username } ).fetchone()

@router_auth.post("/api/signup", status_code=status.HTTP_201_CREATED, response_model=SignUpReturn )
def post_sign_up( creds : Creds,  s : Session = Depends(get_session)  ):
    
    
    if check_username_not_exist(creds.username , s):
        raise HTTPException( status_code=status.HTTP_409_CONFLICT, detail="username already exists" )
    
    s.execute( text("insert into users(username, password) values(:username , :password) ") , { "username" : creds.username, "password" : pwd_context.hash( creds.password ) }  )
    s.commit()
    
    return { "username" : creds.username }


@router_auth.post("/api/login", response_model=LoginReturn)
def login(creds : LoginInput = Depends(validate_login_input),  s : Session = Depends(get_session) ):
    
    print(f"select * from users where binary username = {creds.__dict__['username']}")
    res = s.execute(text("select * from users where binary username = :username"), creds.__dict__ ).mappings().fetchone()
    
    
    if res and pwd_context.verify( creds.password , res['password'] ) :
        
        # token = jwt.encode( { "id" : res['id'] , "exp" : ( datetime.now(timezone.utc) + timedelta(minutes=100) )  },
        #           settings.jwt_secret
        #           ,algorithm="HS256" ) 
        
        token = ecncrypt_jwt_token( { "id" : res['id'] }, settings.jwt_secret, "HS256" )
        
        return {"access_token" : token , "token_type" : "bearer" }
    
    
    raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED )


       


@router_auth.get("/api/protected_test")
def ppp( jwt_token : str = Depends(oauth2_scheme) ) :
    
    decode_jwt_token(jwt_token, settings.jwt_secret, "HS256" )
    
    return {"data" : "protected"}