
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Literal

class Item(BaseModel):
    content: str

class NewItemRequest ( Item ) : 
    pass   
    
class GetAllItemsResponse ( BaseModel ) :
    # items : List[ NewItemRequest ]
    items: List[Item]
    
    
    
class Creds ( BaseModel ) :
    username : str = Field(..., min_length = 4)
    password : str = Field(..., min_length = 4)
    
class LoginInput( BaseModel ) :
    username : str = Field(..., min_length = 1)
    password : str = Field(..., min_length = 1)
    
    
class LoginReturn( BaseModel ):
    access_token: str = Field(... , min_length=10)
    token_type: Literal["bearer"]
    
class SignUpReturn( BaseModel ):
    username : str
    
class NewItemReturn(BaseModel):
    message : Literal["created!"]