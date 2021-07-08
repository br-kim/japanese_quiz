import json

from sqlalchemy.orm import Session

import models
import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_hiragana_score(db: Session, user_id: int):
    return db.query(models.HiraganaScore).filter(models.HiraganaScore.id == user_id).first()


def get_user_katakana_score(db: Session, user_id: int):
    return db.query(models.KatakanaScore).filter(models.KatakanaScore.id == user_id).first()


def create_user_scoreboard(db: Session, user_id: int):
    db_hiragana_scoreboard = models.HiraganaScore(id=user_id)
    db_katakana_scoreboard = models.KatakanaScore(id=user_id)
    db.add(db_hiragana_scoreboard)
    db.add(db_katakana_scoreboard)
    db.commit()
    db.refresh(db_hiragana_scoreboard)
    db.refresh(db_katakana_scoreboard)
    return db_hiragana_scoreboard, db_katakana_scoreboard


def update_user_scoreboard(db: Session, user_id: int, char_type: str, char_name: str):
    db_scoreboard = None
    if char_type == 'hiragana':
        db_scoreboard = db.query(models.HiraganaScore).filter(models.HiraganaScore.id == user_id).first()
    elif char_type == 'katakana':
        db_scoreboard = db.query(models.KatakanaScore).filter(models.KatakanaScore.id == user_id).first()
    else:
        return None
    score = json.loads(db_scoreboard.score)
    score[char_name] += 1
    db_scoreboard.score = json.dumps(score)
    db.commit()
    db.refresh(db_scoreboard)
    return score[char_name]


def create_article(db: Session, article: schemas.ArticleCreate):
    db_article = models.FreeBoard(writer=article.writer, contents=article.contents)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def get_article(db: Session, article_num: int):
    return db.query(models.FreeBoard).filter(models.FreeBoard.id == article_num).first()
