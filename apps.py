import random

import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles  # aiofiles import

import urls
import utils

app = FastAPI()
app.mount("/static", StaticFiles(directory='static'), name="static")
templates = Jinja2Templates(directory='templates')


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get(urls.inf_quiz_page_url)
async def quiz(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})


@app.get(urls.inf_quiz_data_url)
async def new(hiragana: str = None, katakana: str = None):
    result = utils.gen_img_path_list(hiragana, katakana)
    img_path = random.choice(result)
    return {"path": img_path}


@app.get(urls.lim_quiz_page_url)
async def newquiz(request: Request):
    return templates.TemplateResponse("new_quiz.html", {"request": request})


@app.get(urls.lim_quiz_data_url)
async def quizdata(hiragana: str = None, katakana: str = None):
    result = utils.gen_img_path_list(hiragana, katakana)
    random.shuffle(result)
    return {"order": result}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
