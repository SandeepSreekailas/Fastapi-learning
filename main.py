from fastapi import FastAPI

app= FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to FastApi"}


@app.get("/about")
def about():
    return {"message": "Welcome to About"}


#path parameters
@app.get("/books/{book_id}")
def get_book(book_id:int):
    return {"book_id":book_id}

#Query parameters
@app.get("/books")
def get_books(category: str = "all"):
    return {"category":category}

#Request Body with Pydantic
from pydantic import BaseModel

class Book(BaseModel):
    title:str
    author:str
    price:float
#Optional fields in Pydantic
    description:str | None

@app.post("/books")
def create_book(book:Book):
    return {
        "message":"Book added successfully",
        "book":book
    }

#Create a response model
class BookResponse(BaseModel):
    title:str
    author:str


@app.post("/books/preview", response_model=BookResponse)
def preview_book(book: Book):
    return book
