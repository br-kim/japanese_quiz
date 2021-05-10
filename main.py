import random
import os
import json

import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles  # aiofiles import

from dto.charlist import CharList

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/quiz")
async def quiz(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})


@app.get("/quiz/new")
async def new(hiragana: str = None, katakana: str = None):
    result = []
    hiragana_urls = ["./static/img/hiragana/" + i for i in os.listdir("./static/img/hiragana")]
    katakana_urls = ["./static/img/katakana/" + i for i in os.listdir("./static/img/katakana")]
    if hiragana:
        result += hiragana_urls
    if katakana:
        result += katakana_urls
    if hiragana is None and katakana is None:
        result += hiragana_urls
        result += katakana_urls
    img_path = random.choice(result)
    return {"path": img_path}


@app.get("/newquiz")
async def newquiz(request: Request):
    return templates.TemplateResponse("new_quiz.html", {"request": request})


@app.get("/quizdata")
async def quizdata(chars: str = None):
    # if chars:
    #     print(chars)
    #     # a = ["./"+"/".join(i[1:-1].split("src=")[1][1:-1].split("/")[3:]) for i in chars.split(',')]
    #     a = ["./"+"/".join(i.split("/")[3:]) for i in chars.split(',')]
    #     print(a)
    #     return {"order": a}
    hiragana_list = os.listdir("./static/img/hiragana")
    katakana_list = os.listdir("./static/img/katakana")
    all_char = [f"./static/img/hiragana/{char}" for char in hiragana_list] + \
               [f"./static/img/katakana/{char}" for char in katakana_list]
    random.shuffle(all_char)
    return {"order": all_char}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
