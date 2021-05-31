import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles  # aiofiles import
from fastapi.templating import Jinja2Templates
from routers import quiz

app = FastAPI()
app.mount("/static", StaticFiles(directory='static'), name="static")
templates = Jinja2Templates(directory='templates')
app.include_router(quiz.router)


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("apps:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
