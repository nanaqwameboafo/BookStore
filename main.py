from fastapi import FastAPI
from  src.book.routers import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_router
#life span event 
@asynccontextmanager
async def life_span(app:FastAPI):
    print("STARTING SERVER....")
    await init_db()
    yield
    print("SHUTTING DOWN SERVER...")


version = "1.0.0"

app = FastAPI(
    title="Book Management API",
    description="An API to manage a collection of books.",
    version=version,
    lifespan= life_span
)

app.include_router(book_router,prefix=f"/api/{version}/Books",tags=["Books"] )
app.include_router(auth_router,prefix=f"/api/{version}/Users",tags=["Authentication"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Book Management API"}





