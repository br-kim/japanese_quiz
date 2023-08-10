import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

import constants
import models
from routers import quiz, login, community, chatting, user, scoreboard, index, admin
from database import engine
from config import get_settings
from connectionmanager import broadcast
from utils.logging_utils import info_logger, error_logger

models.Base.metadata.create_all(bind=engine)

app = FastAPI(**get_settings().DOCS_SETTING)
app.mount("/static", StaticFiles(directory='static'), name="static")

app.include_router(index.index_router)
app.include_router(quiz.quiz_router)
app.include_router(login.login_router)
app.include_router(community.community_router)
app.include_router(chatting.chatting_router)
app.include_router(user.user_router)
app.include_router(scoreboard.scoreboard_router)
app.include_router(admin.admin_router)

@app.middleware("http")
async def add_user_token_request(request: Request, call_next):
    # 유저 토큰 공간 생성
    try:
        getattr(request.state, "user_token")
    except Exception:
        request.state.user_token = dict()
    response = await call_next(request)
    return response

@app.middleware("http")
async def set_logging(request: Request, call_next):
    method = request.method
    endpoint = request.url.path
    real_ip = request.headers.get("x-real-ip")
    request_query_param = request.query_params
    logging_data_dict = {
        "user_ip": real_ip,
        "method": method,
        "endpoint": endpoint,
        "request_query_param": request_query_param
    }
    info_logger.info(logging_data_dict)
    return await call_next(request)

@app.middleware("http")
async def error_logging(request: Request, call_next):
    try:
        response = await call_next(request)
    except Exception as e:
        error_logger.error(e)
        raise e
    return response

@app.on_event("startup")
async def startup_event():
    await broadcast.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await broadcast.disconnect()


if __name__ == "__main__":
    uvicorn.run("apps:app", host="0.0.0.0", port=constants.PORT_NUMBER, reload=True, proxy_headers=True)

