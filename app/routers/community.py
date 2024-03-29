import html
from typing import Optional, List

from fastapi import APIRouter, Request, Depends, HTTPException, status, Response
from fastapi.templating import Jinja2Templates

import crud
import schemas
from dependencies import get_db
from dependencies import check_user

community_router = APIRouter()
templates = Jinja2Templates(directory='templates')


@community_router.get('/fb')
async def get_freeboard_page(request: Request):
    """
    자유게시판 메인 페이지
    """
    return templates.TemplateResponse('freeboard.html', {'request': request})


@community_router.get('/article')
async def show_article_template(request: Request):
    """
    자유게시판 글 조회 페이지
    """
    return templates.TemplateResponse('article.html', {'request': request})


@community_router.get('/article/edit')
async def show_edit_article_template(request: Request):
    """
    자유게시판 글 수정 페이지
    """
    return templates.TemplateResponse('edit_article.html', {'request': request})


@community_router.get('/freeboard', response_model=schemas.ArticleListResponse)
async def get_article_list(page: Optional[int] = 1, db=Depends(get_db)):
    """
    자유게시판 글 목록 조회 API
    """
    if page < 1:
        page = 1
    total_size = crud.get_all_article_size(db=db)
    offset = 3 * (page - 1)
    result = (total_size // 3) + 1
    articles = crud.get_articles_limit(db=db, offset_value=offset)
    return schemas.ArticleListResponse(articles_length=result, articles=articles)


@community_router.post('/freeboard/write/article', status_code=status.HTTP_201_CREATED)
async def write_article(request: Request, article: schemas.ArticleRequest, db=Depends(get_db), token=Depends(check_user)):
    """
    자유게시판 글 작성 API
    """
    writer = token.get("user_email")
    if not (writer and article.dict().get('title') and article.dict().get('contents')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    db_article = schemas.ArticleCreate(writer=writer, title=html.escape(article.title),
                                       contents=html.escape(article.contents))
    created_article = crud.create_article(db, db_article)
    return created_article.id


@community_router.post('/freeboard/write/comment', status_code=status.HTTP_201_CREATED)
async def write_comment(request: Request, comment: schemas.CommentRequest, db=Depends(get_db), token=Depends(check_user)):
    """
    자유게시판 댓글 작성 API
    """
    writer = token.get("user_email")
    if not (writer and comment.model_dump().get('contents')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    db_comment = schemas.CommentCreate(writer=writer, contents=comment.contents, article_id=comment.article_id,
                                       parent_id=comment.parent_id)
    created_comment = crud.create_comment(db, db_comment)
    return created_comment.id


@community_router.patch('/freeboard/article/{article_id}')
async def edit_article(request: Request,
                       article_id: int, article: schemas.ArticleRequest, db=Depends(get_db), token=Depends(check_user)):
    """
    자유게시판 글 수정 API
    """
    db_article = crud.get_article(db, article_num=article_id)
    if token.get("user_email") == db_article.writer:
        crud.update_article(db=db, article_id=article_id, title=article.title, contents=article.contents)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@community_router.patch('/freeboard/comment/{comment_id}')
async def edit_comment(request: Request, comment_id: int, comment: schemas.CommentEdit, db=Depends(get_db),
                       token=Depends(check_user)):
    """
    자유게시판 댓글 수정 API
    """
    db_comment = crud.get_comment(db=db, comment_id=comment_id)
    if token.get("user_email") == db_comment.writer:
        crud.update_comment(db=db, comment_id=comment_id, contents=comment.contents)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@community_router.delete('/freeboard/article/{article_id}')
async def delete_article(request: Request, article_id: int, db=Depends(get_db), token=Depends(check_user)):
    """
    자유게시판 글 삭제 API
    """
    article = crud.get_article(db=db, article_num=article_id)
    if token.get("user_email") == article.writer:
        crud.delete_article(db=db, article_id=article_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@community_router.delete('/freeboard/comment/{comment_id}')
async def delete_comment(request: Request, comment_id: int, db=Depends(get_db), token=Depends(check_user)):
    """
    자유게시판 댓글 삭제 API
    """
    comment = crud.get_comment(db=db, comment_id=comment_id)
    if token.get("user_email") == comment.writer:
        crud.delete_comment(db=db, comment_id=comment_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@community_router.get('/write')
async def write_page(request: Request):
    """
    자유게시판 글 작성 페이지
    """
    return templates.TemplateResponse('write_article.html', {'request': request})


@community_router.get('/freeboard/{article_id}', response_model=schemas.Article)
async def get_article(article_id: int, db=Depends(get_db), token=Depends(check_user)):
    """
    자유게시판 글 조회 API
    """
    db_article = crud.get_article(db=db, article_num=article_id)
    return schemas.Article.model_validate(db_article)


@community_router.get('/freeboard/{article_id}/comment', response_model=List[schemas.Comment])
async def get_comments(article_id, db=Depends(get_db), token=Depends(check_user)):
    """
    자유게시판 댓글 조회 API
    """
    db_comments = crud.get_comments_by_article_id(db, article_id=article_id)
    return [schemas.Comment.model_validate(comment) for comment in db_comments]
