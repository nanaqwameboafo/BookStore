from fastapi import APIRouter,HTTPException,status,Depends
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from  . schemas import Create_book,UpdateBook,Book
from  . service import BookService
from src.db.main import get_db
from uuid import UUID
from src.auth.depencies import AccessTokenBearer



book_router = APIRouter()

book_service = BookService()
auth = AccessTokenBearer()

@book_router.get("/get",response_model=List[Book])
async def get_all_books(session : AsyncSession = Depends(get_db), 
                        user_details = Depends(auth) ) -> List[Book]:
    book = await book_service.get_all_books(session)
    print(user_details)
    return book
    

@book_router.get("/{book_uid}",response_model=Book)
async def get_book(book_uid: UUID, session:AsyncSession= Depends(get_db), user_deatails = Depends(auth)) -> dict:
    book = await book_service.get_book(book_uid, session)
    if book :
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book id of {book_uid} is not found")
    
  

@book_router.post("/create-book", status_code=status.HTTP_201_CREATED, response_model= Book )
async def create_book(book_data:Create_book,session:AsyncSession= Depends(get_db), user_details = Depends(auth)) :
    new_book = await book_service.create_book(book_data,session)
    return new_book
    
    

@book_router.patch("/update-book", response_model=Book)
async def updates_book(book_uid: UUID, book_data:UpdateBook,session:AsyncSession= Depends(get_db), user_details = Depends(auth)) -> dict:
    book_to_update = await book_service.update_book(book_uid,book_data,session)
    if book_to_update:
        return book_to_update
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Book not found")

@book_router.delete("/delete-book",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid:UUID,session:AsyncSession= Depends(get_db),user_details = Depends(auth)): 
   deleted_book = await book_service.delete_book(book_uid,session)
   if deleted_book is None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
   else:
       return {"deleted successfully"}
   



       