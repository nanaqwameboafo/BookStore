from pydantic import BaseModel,Field,field_validator
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
    password : str = Field(..., min_length=8, description="Password must be at least 8 characters long")
    @field_validator('password')
    @classmethod    
    def password_strength(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        return v


class Login(BaseModel):
    email: str  = Field(max_length=20)
    password : str


class ResetPassword(BaseModel):
    password: str = Field(..., min_length=8, description="New password")
    confirm_password: str = Field(..., min_length=8, description="Confirm new password")
    
    @field_validator('password')
    @classmethod
    def password_strength(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        return v
