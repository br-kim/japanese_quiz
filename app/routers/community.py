import html
from typing import Optional

from fastapi import APIRouter, Request, Depends, HTTPException, status, Response
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
    parent_id: Optional[int]


class CommentEdit(BaseModel):
    contents: str


class DeleteContent(BaseModel):
    content_id: int
    content_writer: str


@community_router.get('/fb')
async def fb(request: Request):
    return templates.TemplateResponse('freeboard.html', {'request': request})


@community_router.get('/article')
async def show_article_template(request: Request):
    return templates.TemplateResponse('article.html', {'request': request})


@community_router.get('/article/edit')
async def show_edit_article_template(request: Request):
    return templates.TemplateResponse('edit_article.html', {'request': request})


@community_router.get('/freeboard')
async def freeboard(page: Optional[int] = 1, db=Depends(get_db)):
    if page < 1:
        page = 1
    total_size = crud.get_all_article_size(db=db)
    offset = 3 * (page - 1)
    return {'articles_length': (total_size - 1) // 3, 'articles': crud.get_articles_limit(db=db, offset_value=offset)}


@community_router.post('/freeboard/write/article', status_code=status.HTTP_201_CREATED)
async def write_article(request: Request, article: Article, db=Depends(get_db)):
    writer = request.state.user_email
    if not (writer and article.dict().get('title') and article.dict().get('contents')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    db_article = schemas.ArticleCreate(writer=writer, title=html.escape(article.title),
                                       contents=html.escape(article.contents))
    created_article = crud.create_article(db, db_article)
    return created_article.id


@community_router.post('/freeboard/write/comment', status_code=status.HTTP_201_CREATED)
async def write_comment(request: Request, comment: Comment, db=Depends(get_db)):
    writer = request.state.user_email
    if not (writer and comment.dict().get('contents')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    db_comment = schemas.CommentCreate(writer=writer, contents=comment.contents, article_id=comment.article_id,
                                       parent_id=comment.parent_id)
    created_comment = crud.create_comment(db, db_comment)
    return created_comment.id


@community_router.patch('/freeboard/edit/article/{article_id}')
async def edit_article(request: Request, article_id: int, article: Article, db=Depends(get_db)):
    db_article = crud.get_article(db, article_num=article_id)
    if request.state.user_email == db_article.writer:
        crud.update_article(db=db, article_id=article_id, title=article.title, contents=article.contents)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@community_router.patch('/freeboard/edit/comment/{comment_id}')
async def edit_comment(request: Request, comment_id: int, comment: CommentEdit, db=Depends(get_db)):
    db_comment = crud.get_comment(db=db, comment_id=comment_id)
    if request.state.user_email == db_comment.writer:
        crud.update_comment(db=db, comment_id=comment_id, contents=comment.contents)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@community_router.delete('/freeboard/delete/{content_type}')
async def delete_content(request: Request, content_type: str, content: DeleteContent, db=Depends(get_db)):
    if request.state.user_email == content.content_writer:
        if content_type == 'article':
            crud.delete_article(db=db, article_id=content.content_id)
        elif content_type == 'comment':
            crud.delete_comment(db=db, comment_id=content.content_id)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@community_router.get('/write')
async def write_page(request: Request):
    return templates.TemplateResponse('write_article.html', {'request': request})


@community_router.get('/freeboard/{article_id}')
async def show_article(article_id: int, db=Depends(get_db)):
    db_article = crud.get_article(db=db, article_num=article_id)
    return db_article


@community_router.get('/freeboard/{article_id}/comment')
async def show_comments(article_id, db=Depends(get_db)):
    db_comments = crud.get_comments_by_article_id(db, article_id=article_id)
    return db_comments
