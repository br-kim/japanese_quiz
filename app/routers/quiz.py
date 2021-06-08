import random


from fastapi import APIRouter, Depends
from fastapi import Request, HTTPException
from fastapi.templating import Jinja2Templates

import urls
import utils
from dependencies import check_user

templates = Jinja2Templates(directory='templates')

quiz_router = APIRouter(dependencies=[Depends(check_user)])


@quiz_router.get(urls.inf_quiz_page_url)
async def quiz(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})


@quiz_router.get(urls.lim_quiz_page_url)
async def newquiz(request: Request):
    return templates.TemplateResponse("new_quiz.html", {"request": request})


@quiz_router.get(f'{urls.QUIZ_DATA_BASE_URL}' + '/{data_type}')
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
