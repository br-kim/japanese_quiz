import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database, create_database
from sqlalchemy import text
from fastapi.testclient import TestClient


import osenv
import models
from models import Base
from utils import create_token
from .database import Session
from crud import create_user_scoreboard, create_article, create_comment
from schemas import ArticleCreate, CommentCreate, Article, Comment

def init_database():
    if not database_exists(str(osenv.TEST_DATABASE_URL)):
        create_database(str(osenv.TEST_DATABASE_URL))


@pytest.fixture(scope="session")
def db():
    if database_exists(str(osenv.TEST_DATABASE_URL)):
        drop_database(str(osenv.TEST_DATABASE_URL))
    init_database()
    engine = create_engine(str(osenv.TEST_DATABASE_URL))
    Base.metadata.create_all(bind=engine)
    Session.configure(bind=engine)
    yield
    drop_database(str(osenv.TEST_DATABASE_URL))


@pytest.fixture(scope="function")
def session(db):
    session = Session()
    session.begin_nested()
    yield session
    session.rollback()
    all_models = Base.metadata.tables.values()
    for model in all_models:
        session.execute(model.delete())
    session.commit()
    session.close()


@pytest.fixture(scope="function")
def client(session):
    from apps import app
    yield TestClient(app)

@pytest.fixture(scope="function")
def create_user(client, session):
    user_email = "test@test.com"
    user_name = "test"
    new_user = models.User(email=user_email)
    session.add(new_user)
    payload = dict(user_email=user_email, user_name=user_name, user_id=new_user.id)
    token = create_token(payload=payload)
    session.commit()
    return token


@pytest.fixture(scope="function")
def create_score(session, create_user):
    user_id = session.query(models.User).first().id
    create_user_scoreboard(session, user_id)
    return create_user

@pytest.fixture(scope="function")
def create_article_fixture(session, create_user):
    user = session.query(models.User).first()
    article = create_article(session, ArticleCreate(writer=user.email,title="test",contents="test"))
    return create_user, Article.model_validate(article)

@pytest.fixture(scope="function")
def create_comment_fixture(session, create_article_fixture):
    token, _ = create_article_fixture
    user = session.query(models.User).first()
    article = session.query(models.FreeBoard).first()
    comment = create_comment(session, CommentCreate(writer=user.email,contents="test",article_id=article.id))
    return token, Comment.model_validate(comment)