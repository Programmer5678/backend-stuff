
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta , timezone
from fastapi.security.oauth2 import  OAuth2PasswordBearer
from fastapi import  HTTPException, status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')  
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated="auto" )

def ecncrypt_jwt_token( myDict, jwt_secret, algo):
    
    
    return jwt.encode( {
                  **myDict,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=100)
                },
                jwt_secret
                ,algorithm=algo )
    

def decode_jwt_token(jwt_token, jwt_secret, algo):
    
    try:
        return jwt.decode(jwt_token, jwt_secret , algorithms=[algo] )

    except:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED , detail="token invalid/expired!", headers={"WWW-Authenticate": "Bearer"}) 
    