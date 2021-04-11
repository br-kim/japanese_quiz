import random
import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles #aiofiles import

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
async def new(request: Request):
    hiragana_list = os.listdir("./static/img/hiragana")
    img = random.choice(hiragana_list)
    img_path = "./static/img/hiragana/" + img
    return {"path": img_path}


@app.get("/newquiz")
async def newquiz(request: Request):
    all_char = []
    hiragana_list = os.listdir("./static/img/hiragana")
    katakana_list = os.listdir("./static/img/katakana")
    all_char = [f"./static/img/hiragana/{char}" for char in hiragana_list] + \
               [f"./static/img/katakana/{char}" for char in katakana_list]
    random.shuffle(all_char)
    return templates.TemplateResponse("new_quiz.html", {"request": request, "order": all_char})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
