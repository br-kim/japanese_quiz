import random


from fastapi import APIRouter

from fastapi import Request, HTTPException

import urls
import utils
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')

router = APIRouter()


@router.get(urls.inf_quiz_page_url)
async def quiz(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})


@router.get(urls.lim_quiz_page_url)
async def newquiz(request: Request):
    return templates.TemplateResponse("new_quiz.html", {"request": request})


@router.get('/quizdata/{data_type}')
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