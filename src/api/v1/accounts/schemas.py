from pydantic import BaseModel,Field
import uuid
from datetime import datetime

class UserCreateModel(BaseModel):
    username:str = Field(max_length=50)
    password:str = Field(min_length=6,max_length=8)

class UserLoginModel(BaseModel):
    username:str = Field(max_length=50)
    password:str = Field(min_length=6,max_length=8)
