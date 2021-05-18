import random
import os
import sys
from typing import Optional

import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles  # aiofiles import


app = FastAPI()
app.mount("/static", StaticFiles(directory='static'), name="static")
templates = Jinja2Templates(directory='templates')


def gen_img_path(gana: str):
    return "./static/img/" + gana


def gen_img_path_list(hiragana: Optional[str], katakana: Optional[str]):
    result = []
    if hiragana:
        result += hiragana_urls
    if katakana:
        result += katakana_urls
    if hiragana is None and katakana is None:
        result += hiragana_urls
        result += katakana_urls
    return result


hiragana_url = gen_img_path('hiragana')
katakana_url = gen_img_path('katakana')

hiragana_urls = [hiragana_url+"/" + i for i in os.listdir(hiragana_url)]
katakana_urls = [katakana_url+"/" + i for i in os.listdir(katakana_url)]


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/quiz")
async def quiz(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})


@app.get("/quiz/new")
async def new(hiragana: str = None, katakana: str = None):
    result = gen_img_path_list(hiragana, katakana)
    img_path = random.choice(result)
    return {"path": img_path}


@app.get("/newquiz")
async def newquiz(request: Request):
    return templates.TemplateResponse("new_quiz.html", {"request": request})


@app.get("/quizdata")
async def quizdata(hiragana: str = None, katakana: str = None):
    result = gen_img_path_list(hiragana, katakana)
    random.shuffle(result)
    return {"order": result}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
