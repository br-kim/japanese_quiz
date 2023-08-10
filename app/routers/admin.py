from typing import List

from fastapi import APIRouter, Request, Depends

from dependencies import check_admin, get_db
import schemas
import crud

admin_router = APIRouter(prefix="/admin")

@admin_router.get("/users", response_model=List[schemas.User])
async def get_users(request: Request,db=Depends(get_db), token=Depends(check_admin)):
    """
    모든 유저 정보 확인
    """
    return crud.get_user_all(db)

