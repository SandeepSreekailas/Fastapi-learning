from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])



def get_current_user():
    return {"username": "fakecurrentuser"}