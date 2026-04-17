from pydantic import BaseModel, HttpUrl, Field
# from typing import Any, List, Literal
# from datetime import date, datetime

class PathsRequestModel(BaseModel):
    input_path: str
    output_path: str

class CreatedResponseModel(BaseModel):
    created: str