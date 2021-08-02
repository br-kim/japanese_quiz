import random
import base64
import os
import json

from fastapi import APIRouter, Depends, Response, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel

import urls
import utils
import crud
from dependencies import check_user, get_db

templates = Jinja2Templates(directory='templates')

quiz_router = APIRouter(dependencies=[Depends(check_user)])


class AnswerRes(BaseModel):
    csrf_token: str
    character: str
    quiz_type: str


@quiz_router.get(urls.inf_quiz_page_url)
async def quiz(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})


@quiz_router.get(urls.lim_quiz_page_url)
async def new_quiz(request: Request):
    return templates.TemplateResponse("new_quiz.html", {"request": request})


@quiz_router.get(urls.QUIZ_DATA_BASE_URL + '/{data_type}')
async def path_data(request: Request, data_type: str, kind: str = 'all', is_weighted: str = '',
                    db: Session = Depends(get_db)):
    result = utils.gen_img_path_list(kind)
    csrf_token = base64.b64encode(os.urandom(8)).decode()
    request.session['csrf_token'] = csrf_token
    if data_type == "path":
        if is_weighted:
            cur_user_email = request.session.get('user_email')
            cur_user = crud.get_user_by_email(db=db, email=cur_user_email)
            weight = []
            total_score = 0
            score_values = []
            if kind == 'hiragana' or kind == 'all':
                hira_score_db = crud.get_user_hiragana_score(db=db, user_id=cur_user.id)
                score_dict = json.loads(hira_score_db.score)
                score_values += list(score_dict.values())
                total_score += sum(score_values)
            if kind == 'katakana' or kind == 'all':
                kata_score_db = crud.get_user_katakana_score(db=db, user_id=cur_user.id)
                score_dict = json.loads(kata_score_db.score)
                score_values += list(score_dict.values())
                total_score += sum(score_dict.values())
            weight += [total_score - i for i in score_values]
            img_path = random.choices(result, weight).pop()
        else:
            img_path = random.choice(result)
        return {"path": img_path, "csrf_token": csrf_token}

    elif data_type == "path-list":
        random.shuffle(result)
        return {"order": result, "csrf_token": csrf_token}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Type")


@quiz_router.get('/scoreboard')
async def scoreboard(request: Request, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db=db, email=request.session.get('user_email'))
    hira_score = crud.get_user_hiragana_score(db=db, user_id=user.id)
    kata_score = crud.get_user_katakana_score(db=db, user_id=user.id)

    return templates.TemplateResponse("scoreboard.html", {
        "request": request,
        "hiragana_score": json.loads(hira_score.score),
        "katakana_score": json.loads(kata_score.score)
    })


@quiz_router.patch('/scoreupdate')
async def score_update(request: Request, response: AnswerRes, db: Session = Depends(get_db)):
    token = request.session.get('csrf_token')
    if token is not None and response.quiz_type != '/newquiz':
        request.session.pop('csrf_token')
    if response.csrf_token == token:
        char_data = response.character.split('/')[-2:]
        char_type = char_data[0]
        char_name = char_data[1].split('.')[0]
        current_user = crud.get_user_by_email(db=db, email=request.session.get('user_email'))
        user_id = current_user.id
        result = crud.update_user_scoreboard(db=db, user_id=user_id, char_type=char_type, char_name=char_name)
        if result is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Access")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
