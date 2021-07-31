import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

import osenv
from routers import quiz, login, community
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory='static'), name="static")
templates = Jinja2Templates(directory='templates')
app.include_router(quiz.quiz_router)
app.include_router(login.login_router)
app.include_router(community.community_router)
app.add_middleware(SessionMiddleware, secret_key=osenv.SESSION_KEY)


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("apps:app", host="0.0.0.0", port=osenv.PORT_NUMBER)
