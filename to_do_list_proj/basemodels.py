
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class Item(BaseModel):
    content: str

class NewItemRequest ( Item ) : 
    pass   
    
class getAllItemsResponse ( BaseModel ) :
    # items : List[ NewItemRequest ]
    items: List[Item]
    
    
    
class Creds ( BaseModel ) :
    username : str = Field(..., min_length = 4)
    password : str = Field(..., min_length = 4)