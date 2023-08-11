from fastapi import APIRouter

from .admin import admin_router
from .user import user_router
from .chatting import chatting_router
from .community import community_router
from .index import index_router
from .login import login_router
from .quiz import quiz_router
from .scoreboard import scoreboard_router
from .user import user_router

api_router = APIRouter()

api_router.include_router(admin_router)
api_router.include_router(user_router)
api_router.include_router(chatting_router)
api_router.include_router(community_router)
api_router.include_router(index_router)
api_router.include_router(login_router)
api_router.include_router(quiz_router)
api_router.include_router(scoreboard_router)
api_router.include_router(user_router)
