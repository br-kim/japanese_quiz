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
async def new():
    hiragana_list = os.listdir("./static/img/hiragana")
    img = random.choice(hiragana_list)
    img_path = "./static/img/hiragana/" + img
    return {"path": img_path}


@app.get("/newquiz")
async def newquiz(request: Request):
    return templates.TemplateResponse("new_quiz.html", {"request": request})


@app.get("/quizdata")
async def quizdata(chars: str = None):
    if chars:
        a = ["./"+"/".join(i[1:-1].split("src=")[1][1:-1].split("/")[3:]) for i in chars.split(',')]
        return {"order": a}
    hiragana_list = os.listdir("./static/img/hiragana")
    katakana_list = os.listdir("./static/img/katakana")
    all_char = [f"./static/img/hiragana/{char}" for char in hiragana_list] + \
               [f"./static/img/katakana/{char}" for char in katakana_list]
    random.shuffle(all_char)
    return {"order": all_char}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
