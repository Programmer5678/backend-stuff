from fastapi import HTTPException, status, Depends
from fastapi.params import Body
from sqlalchemy import text
from sqlalchemy.orm import Session

from settings import settings
from engine_and_session import get_session
from basemodels import NewItemRequest, GetAllItemsResponse, NewItemReturn
from handle_fastapi_auth import decode_jwt_token, oauth2_scheme

def create_app_endpoints(app):
    @app.get("/api")
    def g():
        return {"message": "blah"}  

    @app.post("/api/old", status_code=status.HTTP_201_CREATED)
    def old_new_item(payload: dict = Body(...), s: Session = Depends(get_session)):
        if "content" not in payload:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="message invalid - no content passed..."
            )
        
        print("password: ", settings.mysql_pass)
        s.execute(text("INSERT INTO testing (content) VALUES (:content)"), {"content": payload["content"]})
        s.commit()
        return {"message": "created!"}

    @app.get("/api/main", response_model=GetAllItemsResponse)
    def get_all_items(s: Session = Depends(get_session), jwt_token: str = Depends(oauth2_scheme)):
        decoded = decode_jwt_token(jwt_token, settings.jwt_secret, "HS256")
        res = s.execute(text("select content from items where user_id = :id"), decoded).mappings().fetchall()
        return {"items": res}

    @app.post("/api/main", status_code=status.HTTP_201_CREATED, response_model=NewItemReturn)
    def new_item(item: NewItemRequest, s: Session = Depends(get_session), jwt_token: str = Depends(oauth2_scheme)):
        user_id = decode_jwt_token(jwt_token, settings.jwt_secret, "HS256")["id"]
        s.execute(text("INSERT INTO items (content, user_id) VALUES (:content, :user_id)"),
                  {"content": item.content, "user_id": user_id})
        s.commit()
        return {"message": "created!"}