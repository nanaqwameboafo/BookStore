
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
import uuid



class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    language: str
    created_at : datetime
    updated_at :datetime

    


class Create_book(BaseModel):

    title: str
    author: str
    publisher: str
    published_date : date  
    language: str

    
    
class RespondBook(BaseModel):
    title: str
    author: str
    publisher: str
   
    class Config:
        orm_mode = True

class UpdateBook(BaseModel):
    title: str
    author: str
    
    