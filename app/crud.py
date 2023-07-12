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
    return db.query(models.HiraganaScore).filter(models.HiraganaScore.user_id == user_id).first()


def get_user_katakana_score(db: Session, user_id: int):
    return db.query(models.KatakanaScore).filter(models.KatakanaScore.user_id == user_id).first()


def create_user_scoreboard(db: Session, user_id: int):
    db_hiragana_scoreboard = models.HiraganaScore(user_id=user_id)
    db_katakana_scoreboard = models.KatakanaScore(user_id=user_id)
    db.add(db_hiragana_scoreboard)
    db.add(db_katakana_scoreboard)
    db.commit()
    db.refresh(db_hiragana_scoreboard)
    db.refresh(db_katakana_scoreboard)
    return db_hiragana_scoreboard, db_katakana_scoreboard


def update_user_scoreboard(db: Session, user_id: int, char_type: str, char_name: str):
    if char_type == 'hiragana':
        db_scoreboard = db.query(models.HiraganaScore).filter(models.HiraganaScore.user_id == user_id).first()
    elif char_type == 'katakana':
        db_scoreboard = db.query(models.KatakanaScore).filter(models.KatakanaScore.user_id == user_id).first()
    else:
        raise ValueError
    score = json.loads(db_scoreboard.score)
    score[char_name] += 1
    db_scoreboard.score = score
    db.commit()
    db.refresh(db_scoreboard)
    return score[char_name]


def create_article(db: Session, article: schemas.ArticleCreate):
    db_article = models.FreeBoard(writer=article.writer, contents=article.contents, title=article.title)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def get_article(db: Session, article_num: int):
    return db.query(models.FreeBoard).filter(models.FreeBoard.id == article_num).first()


def get_articles_limit(db: Session, offset_value: int):
    return db.query(models.FreeBoard).order_by(models.FreeBoard.id.desc()).offset(offset_value).limit(3).all()


def get_all_article_size(db: Session):
    return db.query(models.FreeBoard).count()


def update_article(db: Session, article_id: int, title: str, contents: str):
    article = get_article(db, article_id)
    article.contents = contents
    article.title = title
    db.commit()
    db.refresh(article)
    return article


def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = models.Comment(writer=comment.writer, contents=comment.contents, article_id=comment.article_id,
                                parent_id=comment.parent_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


def get_comments_by_article_id(db: Session, article_id: int):
    return db.query(models.Comment).filter(models.Comment.article_id == article_id).order_by(models.Comment.id).all()


def update_comment(db: Session, comment_id: int, contents: str):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    db_comment.contents = contents
    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete_article(db: Session, article_id: int):
    db_article = db.query(models.FreeBoard).filter(models.FreeBoard.id == article_id).first()
    db.delete(db_article)
    db.commit()
    return


def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    db.delete(db_comment)
    db.commit()
    return
