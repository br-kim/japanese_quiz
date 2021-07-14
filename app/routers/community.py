import html
from typing import Optional

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import crud
import schemas
from dependencies import get_db
from dependencies import check_user

community_router = APIRouter(dependencies=[Depends(check_user)])
templates = Jinja2Templates(directory='templates')


class Article(BaseModel):
    title: str
    contents: str


class Comment(BaseModel):
    contents: str
    article_id: int


@community_router.get('/fb')
async def fb(request: Request):
    return templates.TemplateResponse('freeboard.html', {'request': request})


@community_router.get('/article')
async def show_article(request: Request):
    return templates.TemplateResponse('article.html', {'request': request})


@community_router.get('/freeboard')
async def freeboard(page: Optional[int] = 1, db=Depends(get_db)):
    total_size = crud.get_all_article_size(db=db)
    offset = 3 * (page - 1)
    return {'articles_length': total_size // 3, 'articles': crud.get_articles_limit(db=db, offset_value=offset)}


@community_router.post('/freeboard/write/article', status_code=status.HTTP_201_CREATED)
async def write_article(request: Request, article: Article, db=Depends(get_db)):
    writer = request.session.get('user_email')
    if not (writer and article.dict().get('title') and article.dict().get('contents')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    db_article = schemas.ArticleCreate(writer=writer, title=html.escape(article.title),
                                       contents=html.escape(article.contents))
    created_article = crud.create_article(db, db_article)
    return created_article.id


@community_router.post('/freeboard/write/comment', status_code=status.HTTP_201_CREATED)
async def write_comment(request: Request, comment: Comment, db=Depends(get_db)):
    print(comment)
    writer = request.session.get('user_email')
    if not (writer and comment.dict().get('contents')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    db_comment = schemas.CommentCreate(writer=writer, contents=comment.contents, article_id=comment.article_id)
    created_comment = crud.create_comment(db, db_comment)
    return created_comment.id


@community_router.get('/freeboard/{article_num}')
async def show_article(article_num, db=Depends(get_db)):
    db_article = crud.get_article(db=db, article_num=article_num)
    return db_article


@community_router.get('/freeboard/{article_num}/comment')
async def show_comments(article_num, db=Depends(get_db)):
    db_comments = crud.get_comments_by_article_id(db, article_id=article_num)
    return db_comments


@community_router.get('/write')
async def write_page(request: Request):
    return templates.TemplateResponse('write_article.html', {'request': request})
