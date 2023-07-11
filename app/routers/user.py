from fastapi import APIRouter, Request

user_router = APIRouter()

@user_router.get("/user-info")
async def get_user_info(request: Request):
    user_info = request.state.user_token.get("user_email")
    return user_info