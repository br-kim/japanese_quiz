import random
import base64
import os
import json

from fastapi import APIRouter, Depends, Response, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import urls
import utils
import crud
from dependencies import check_user, get_db

templates = Jinja2Templates(directory='templates')

quiz_router = APIRouter(dependencies=[Depends(check_user)])


@quiz_router.get(urls.inf_quiz_page_url)
async def quiz(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})


@quiz_router.get(urls.lim_quiz_page_url)
async def new_quiz(request: Request):
    return templates.TemplateResponse("new_quiz.html", {"request": request})


@quiz_router.get(urls.QUIZ_DATA_BASE_URL+'/{data_type}')
async def path_data(request: Request, data_type: str, kind: str = None):
    result = utils.gen_img_path_list(kind)
    csrf_token = base64.b64encode(os.urandom(8)).decode()
    request.session['csrf_token'] = csrf_token
    if data_type == "path":
        img_path = random.choice(result)
        return {"path": img_path, "csrf_token": csrf_token}

    elif data_type == "path-list":
        random.shuffle(result)
        return {"order": result, "csrf_token": csrf_token}

    else:
        raise HTTPException(status_code=404, detail="Invalid Kind")


@quiz_router.get('/scoreboard')
async def scoreboard(request: Request, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db=db, email=request.session.get('user_email'))
    hira_score = crud.get_user_hiragana_score(db=db, user_id=user.id)
    kata_score = crud.get_user_katakana_score(db=db, user_id=user.id)

    return {
        "hiragana_score": json.loads(hira_score.score),
        "katakana_score": json.loads(kata_score.score)
    }


@quiz_router.patch('/scoreupdate')
async def score_update(request: Request, db: Session = Depends(get_db)):
    res_json = await request.json()
    if res_json['csrf_token'] == request.session['csrf_token']:
        char_data = res_json['character'].split('/')[-2:]
        char_type = char_data[0]
        char_name = char_data[1].split('.')[0]
        current_user = crud.get_user_by_email(db=db, email=request.session.get('user_email'))
        user_id = current_user.id
        result = crud.update_user_scoreboard(db=db, user_id=user_id, char_type=char_type, char_name=char_name)
        if result is None:
            raise HTTPException(status_code=400, detail="Bad Request")
    else:
        raise HTTPException(status_code=404, detail="Invalid Access")
    return Response(status.HTTP_204_NO_CONTENT)
