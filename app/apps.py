import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import osenv
from routers import quiz, login, community, chatting, user
import models
from database import engine, redis_connection

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory='static'), name="static")
templates = Jinja2Templates(directory='templates')
app.include_router(quiz.quiz_router)
app.include_router(login.login_router)
app.include_router(community.community_router)
app.include_router(chatting.chatting_router)
app.include_router(user.user_router)

@app.middleware("http")
async def add_user_token_request(request: Request, call_next):
    # 유저 토큰 공간 생성
    try:
        getattr(request.state, "user_token")
    except Exception:
        request.state.user_token = dict()
    print(request.state.user_token, "middleware")
    response = await call_next(request)
    return response

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.on_event("startup")
async def startup_event():
    await redis_connection.delete("users")


if __name__ == "__main__":
    uvicorn.run("apps:app", host="0.0.0.0", port=osenv.PORT_NUMBER, workers=1, reload=True)
