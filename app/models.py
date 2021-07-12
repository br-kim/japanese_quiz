import os
import json

from sqlalchemy import Column, Integer, String, JSON, UnicodeText

from database import Base

hiragana_data = dict.fromkeys([file_name.split('.')[0] for file_name in os.listdir('static/img/hiragana')], 0)
katakana_data = dict.fromkeys([file_name.split('.')[0] for file_name in os.listdir('static/img/katakana')], 0)


class User(Base):
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


class FreeBoard(Base):
    __tablename__ = "freeboard"

    id: Column = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    contents = Column(UnicodeText)
    writer = Column(String)
