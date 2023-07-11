from fastapi import APIRouter, Request, Depends
from dependencies import check_user

user_router = APIRouter()

@user_router.get("/user-info")
async def get_user_info(request: Request, token=Depends(check_user)):
    return token.get("user_email")
