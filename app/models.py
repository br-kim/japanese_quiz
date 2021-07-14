import os
import json
from typing import Type

from sqlalchemy import Column, Integer, String, JSON, UnicodeText, func, DateTime

from database import Base

hiragana_data = dict.fromkeys([file_name.split('.')[0] for file_name in os.listdir('static/img/hiragana')], 0)
katakana_data = dict.fromkeys([file_name.split('.')[0] for file_name in os.listdir('static/img/katakana')], 0)


class TimestampMixin(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    created_at = Column(DateTime, default=func.now())


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)


class HiraganaScore(Base):
    __tablename__ = "hiragana"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(String, server_default=json.dumps(hiragana_data))


class KatakanaScore(Base):
    __tablename__ = "katakana"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(String, server_default=json.dumps(katakana_data))


class FreeBoard(TimestampMixin, Base):
    __tablename__ = "freeboard"

    id: Column = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    contents = Column(UnicodeText)
    writer = Column(String)


class Comment(TimestampMixin, Base):
    __tablename__ = "comment"

    id: Column = Column(Integer, primary_key=True, index=True)
    contents = Column(UnicodeText)
    writer = Column(String)
    article_id = Column(Integer, index=True)
