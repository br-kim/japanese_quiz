import json

from fastapi import Request, APIRouter, Depends, HTTPException, status, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import crud
from dependencies import get_db, check_user
from schemas import ScoreData, AnswerRes

scoreboard_router = APIRouter()
templates = Jinja2Templates(directory='templates')


@scoreboard_router.get('/scoreboard')
async def scoreboard(request: Request):
    """
    Scoreboard 페이지 리턴
    """
    return templates.TemplateResponse("scoreboard.html", {
        "request": request,
    })


@scoreboard_router.get("/scoreboard/data")
async def get_scoreboard_data(db: Session = Depends(get_db), token=Depends(check_user)):
    """
    Scoreboard 데이터 API
    """
    user = crud.get_user_by_email(db=db, email=token.get("user_email"))
    hira_score = crud.get_user_hiragana_score(db=db, user_id=user.id)
    kata_score = crud.get_user_katakana_score(db=db, user_id=user.id)
    return ScoreData(hiragana=hira_score.score, katakana=kata_score.score)


@scoreboard_router.patch('/scoreboard/data')
async def score_update(response: AnswerRes, db: Session = Depends(get_db), token=Depends(check_user)):
    """
    Scoreboard 데이터 업데이트 API
    """
    char_data = response.character.split('/')[-2:]
    char_type = char_data[0]
    char_name = char_data[1].split('.')[0]
    user_email = token.get("user_email")
    current_user = crud.get_user_by_email(db=db, email=user_email)
    user_id = current_user.id
    crud.update_user_scoreboard(db=db, user_id=user_id, char_type=char_type, char_name=char_name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
