from fastapi import Request
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

import pytest

from ..apps import app
from ..database import Base
import dependencies
import crud
import models


def check_user():
    return True


@pytest.fixture(scope="session")
def session():
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@127.0.0.1"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    conn = engine.connect()
    conn.execute('commit')
    try:
        conn.execute("create database test_db")
    except:
        pass
    finally:
        conn.close()

    Base.metadata = models.Base.metadata
    engine = create_engine(SQLALCHEMY_DATABASE_URL + "/test_db")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    client = TestClient(app)
    app.dependency_overrides[dependencies.check_user] = check_user
    app.dependency_overrides[dependencies.get_db] = override_get_db
    db = TestingSessionLocal()
    crud.create_user(db, models.User(email='idle947@gmail.com'))
    yield db
    db.close()
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    conn = engine.connect()
    conn.execute('commit')
    conn.execute("drop database test_db with (force)")


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        c.get('/for_test')
        yield c


@app.get('/for_test')
async def for_test(request: Request):
    request.session['user_email'] = 'idle947@gmail.com'
    return "complete"


def test_db_insert_and_get_article(session):
    session = session
    fixture = {'id': 1, 'contents': 'hello', 'writer': 'test@test.com', 'title': 'test-title'}
    article = models.FreeBoard(**fixture)
    crud.create_article(session, article)
    article = crud.get_article(db=session, article_num=1)
    assert article.id == fixture['id'] and article.contents == fixture['contents'] and \
           article.writer == fixture['writer'] and article.title == fixture['title']


def test_db_inset_and_get_comment(session):
    session = session
    fixture = {'id': 1, 'contents': 'hello', 'writer': 'test@test.com', 'article_id': 1}
    comment = models.Comment(**fixture)
    crud.create_comment(session, comment)
    comment = crud.get_comment(db=session, comment_id=1)
    assert comment.id == fixture['id'] and comment.contents == fixture['contents'] and \
           comment.writer == fixture['writer']


def test_api_article(session, client):
    data = {'title': 'hello', 'contents': 'hello'}
    res = client.get('/for_test')
    res = client.post('/freeboard/write/article', json=data)
    assert res.status_code == 201
    res = client.get('/freeboard/1')
    print(res.json())
    assert res
