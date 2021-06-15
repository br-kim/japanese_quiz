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
