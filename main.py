from fastapi import FastAPI, Depends

# app= FastAPI()


# @app.get("/")
# def home():
#     return {"message": "Welcome to FastApi"}


# @app.get("/about")
# def about():
#     return {"message": "Welcome to About"}


# #path parameters
# @app.get("/books/{book_id}")
# def get_book(book_id:int):
#     return {"book_id":book_id}

# #Query parameters
# @app.get("/books")
# def get_books(category: str = "all"):
#     return {"category":category}

# #Request Body with Pydantic
# from pydantic import BaseModel
# from fastapi import status

# class Book(BaseModel):
#     title:str
#     author:str
#     price:float
# #Optional fields in Pydantic
#     description:str | None

# @app.post("/books",status_code=status.HTTP_201_CREATED)
# def create_book(book:Book):
#     return {
#         "message":"Book added successfully",
#         "book":book
#     }

# #Create a response model
# class BookResponse(BaseModel):
#     title:str
#     author:str


# @app.post("/books/preview", response_model=BookResponse)
# def preview_book(book: Book):
#     return book

# #put
# @app.put("/books/{book_id}")
# def update_book(book_id:int,book:Book):
#     return{
#         "message":"Book Replaced",
#         "book_id":book_id,
#         "book name":book
#     }

# #patch
# class BookUpdate(BaseModel):
#     title: str | None = None
#     author: str | None = None
#     price: float | None = None

# @app.patch("/books/{book_id}")
# def part_upd_book(book_id:int,book:BookUpdate):
#     changes=book.model_dump(exclude_unset=True)
#     return {
#         "message":"Book Replaced",
#         "book_id":book_id,
#         "changes":changes
#     }

# #Delete
# @app.delete("/books/{book_id}")
# def delete_book(book_id: int):
#     return {
#         "message": "Book deleted",
#         "book_id": book_id
#     }


# #Error handling with HTTPException
# from fastapi import HTTPException

# @app.get("/boooks/{book_id}")
# def get_boooks(book_id:int):
#     if book_id  !=1:
#         raise HTTPException(
#             status_code=404,
#             detail="book not found"
#         )
#     return{
#         "book_id":1,
#         "title":"Basic Python"
#     }

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


# APIRouter and project structure
# from books import router as bookrouter

# app.include_router(bookrouter)

# @app.get("/")
# def home():
#     return {"message": "Welcome to FastApi"}
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# from users import router as userrouter
# from users import get_current_user

# app.include_router(userrouter)

# @app.get('/profile')
# def get_profile(user: dict=Depends(get_current_user)):
#     return {
#         "profile":user
#     }

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# from middleware import log_request

# app.middleware("http")(log_request)

# @app.get("/")
# def home():
#     return{"messsge":"welcome to home"}


# @app.get("/books")
# def get_books():
#     return {"books": ["Python", "Django"]}

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

from config import settings

app=FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

@app.get("/")
def home():
    return {
        "app_name": settings.app_name,
        "debug": settings.debug
    }