from fastapi import APIRouter, Request, Depends

from dependencies import check_user, get_db
import schemas
import crud

user_router = APIRouter()

@user_router.get("/user-info", response_model=schemas.UserInfoResponse)
async def get_user_info(request: Request, db=Depends(get_db), token=Depends(check_user)):
    """
    유저 정보 API
    """
    user = crud.get_user_by_email(db, token.get("user_email"))
    return schemas.UserInfoResponse(email=user.email, permission=user.permission)
