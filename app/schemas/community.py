from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class ArticleBase(BaseModel):
    writer: str
    title: str
    contents: str


class ArticleCreate(ArticleBase):
    pass


class Article(ArticleBase):
    created_at: datetime
    id: int

    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    writer: str
    contents: str
    article_id: int
    parent_id: int | None = None


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    created_at: datetime
    id: int

    class Config:
        from_attributes = True


class ArticleRequest(BaseModel):
    title: str
    contents: str


class CommentRequest(BaseModel):
    contents: str
    article_id: int
    parent_id: int | None = None


class CommentEdit(BaseModel):
    contents: str

class ArticleListResponse(BaseModel):
    articles_length: int
    articles: List[Article]
