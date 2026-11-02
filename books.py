from fastapi import APIRouter

router = APIRouter(prefix="/books",tags=["books"])

@router.get("/")
def get_books():
    return {"books": ["Python", "Django"]}

@router.get("/{book_id}")
def get_book(book_id: int):
    return {"book_id": book_id}