import random
import base64
import os
import json
from typing import Optional

from fastapi import APIRouter, Depends, Response, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from schemas import ScoreData

import utils
import crud
from dependencies import check_user, get_db, check_user_optional_token

templates = Jinja2Templates(directory='templates')

quiz_router = APIRouter()


class AnswerRes(BaseModel):
    character: str
    quiz_type: str


@quiz_router.get("/quiz")
async def quiz(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request})


@quiz_router.get("/newquiz")
async def test_mode(request: Request):
    return templates.TemplateResponse("test_mode.html", {"request": request})


@quiz_router.get("/quiz-data/random")
async def random_quiz_data(request: Request, kind: str = "all", is_weighted: Optional[str] = None,
                           db: Session = Depends(get_db), token=Depends(check_user_optional_token)):
    result = utils.gen_img_path_list(kind)
    if not token:
        img_path = random.choice(result)
        return {"path": img_path}

    if is_weighted:
        cur_user_email = token.get("user_email")
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
        # 모든 weight 가 0인 경우 None
        if sum(weight) == 0:
            weight = None
        img_path = random.choices(result, weight).pop()
    else:
        img_path = random.choice(result)
    return {"path": img_path}


@quiz_router.get("/quiz-data/test-mode")
async def quiz_test_mode_data(request: Request, kind: str = "all",
                              db: Session = Depends(get_db), token=Depends(check_user)):
    result = utils.gen_img_path_list(kind)
    random.shuffle(result)
    return {"order": result}


@quiz_router.get('/scoreboard')
async def scoreboard(request: Request, db: Session = Depends(get_db)):
    """
    Scoreboard 페이지 리턴
    """
    return templates.TemplateResponse("scoreboard.html", {
        "request": request,
    })


@quiz_router.get("/scoreboard/data")
async def scoreboard_data(request: Request, db: Session = Depends(get_db), token=Depends(check_user)):
    user = crud.get_user_by_email(db=db, email=request.state.user_token.get("user_email"))
    hira_score = crud.get_user_hiragana_score(db=db, user_id=user.id)
    kata_score = crud.get_user_katakana_score(db=db, user_id=user.id)
    return ScoreData(hiragana=json.loads(hira_score.score), katakana=json.loads(kata_score.score))


@quiz_router.patch('/scoreupdate')
async def score_update(request: Request, response: AnswerRes, db: Session = Depends(get_db), token=Depends(check_user)):
    char_data = response.character.split('/')[-2:]
    char_type = char_data[0]
    char_name = char_data[1].split('.')[0]
    user_email = token.get("user_email")
    current_user = crud.get_user_by_email(db=db, email=user_email)
    user_id = current_user.id
    result = crud.update_user_scoreboard(db=db, user_id=user_id, char_type=char_type, char_name=char_name)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
