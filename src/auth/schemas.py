from pydantic import BaseModel,Field
from datetime import datetime
import uuid
from datetime import datetime


class UserResponds(BaseModel):
    uid: uuid.UUID
    username: str
    First_name: str
    Last_name: str
    email: str 
    password_hash : str 
    is_verify: bool 
    Created_at : datetime 
    Updated_at : datetime 



class CreateUser(BaseModel):
    username: str = Field(max_length=10)
    First_name: str  = Field(max_length= 15)
    Last_name: str  = Field(max_length=15)
    email: str  = Field(max_length=20)
    password : str


class Login(BaseModel):
    email: str  = Field(max_length=20)
    password : str
