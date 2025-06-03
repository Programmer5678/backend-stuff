from fastapi.security.oauth2 import OAuth2PasswordRequestForm,  OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from basemodels import LoginInput

def validate_login_input(form: OAuth2PasswordRequestForm = Depends()) -> LoginInput:
    
    try:
        return LoginInput(username=form.username, password=form.password)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Validation failed")