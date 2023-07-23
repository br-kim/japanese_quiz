from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class HiraganaScoreBase(BaseModel):
    score: str


class HiraganaScoreBoardCreate(HiraganaScoreBase):
    pass


class HiraganaScore(HiraganaScoreBase):
    id: int

    class Config:
        orm_mode = True


class KatakanaScoreBase(BaseModel):
    score: str


class KatakanaScoreBoardCreate(KatakanaScoreBase):
    pass


class KatakanaScore(KatakanaScoreBase):
    id: int

    class Config:
        orm_mode = True


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
        orm_mode = True


class CommentBase(BaseModel):
    writer: str
    contents: str
    article_id: int
    parent_id: Optional[int]


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    created_at: datetime
    id: int

    class Config:
        orm_mode = True


class ScoreData(BaseModel):
    hiragana: dict
    katakana: dict

    class Config:
        orm_mode = True


class AnswerRes(BaseModel):
    character: str
    quiz_type: str
