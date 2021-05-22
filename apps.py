import random

import uvicorn
from fastapi import FastAPI, Request, HTTPException
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
async def new(kind: str = None):
    print(kind)
    result = utils.gen_img_path_list(kind)
    if not result:
        raise HTTPException(status_code=404, detail="Invalid Params")
    img_path = random.choice(result)
    return {"path": img_path}


@app.get(urls.lim_quiz_page_url)
async def newquiz(request: Request):
    return templates.TemplateResponse("new_quiz.html", {"request": request})


@app.get(urls.lim_quiz_data_url)
async def quizdata(kind: str = None):
    result = utils.gen_img_path_list(kind)
    if not result:
        raise HTTPException(status_code=404, detail="Invalid Params")
    random.shuffle(result)
    return {"order": result}


@app.get('/quizdata/{data_type}')
async def pathdata(data_type: str, kind: str = None):
    result = utils.gen_img_path_list(kind)
    if data_type == "path":
        img_path = random.choice(result)
        return {"path": img_path}

    elif data_type == "path-list":
        random.shuffle(result)
        return {"order": result}

    else:
        raise HTTPException(status_code=404, detail="Invalid Kind")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
