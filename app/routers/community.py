from fastapi import APIRouter, Request,Depends
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import crud
import schemas
from dependencies import get_db
from dependencies import check_user


community_router = APIRouter()
templates = Jinja2Templates(directory='templates')
quiz_router = APIRouter(dependencies=[Depends(check_user)])


class Article(BaseModel):
    contents: str


@community_router.get('/freeboard')
async def freeboard(request: Request):
    return templates.TemplateResponse("freeboard.html", {'request': request})


@community_router.post('/freeboard/write')
async def write_article(request: Request, article: Article, db=Depends(get_db)):
    writer = request.session.get('user_email')
    db_article = schemas.ArticleCreate(writer=writer, contents=article.contents)
    crud.create_article(db, db_article)
    return None


@community_router.get('/freeboard/{article_num}')
async def show_article(article_num, db=Depends(get_db)):
    db_article = crud.get_article(db=db, article_num=article_num)
    return db_article