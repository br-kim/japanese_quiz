from fastapi import APIRouter, Request, Depends

from dependencies import check_user
import schemas

user_router = APIRouter()

@user_router.get("/user-info", response_model=schemas.UserInfoResponse)
async def get_user_info(request: Request, token=Depends(check_user)):
    """
    유저 정보 API
    """
    return schemas.UserInfoResponse(email=token.get("user_email"))
