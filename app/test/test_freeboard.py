from fastapi import Request
from fastapi.testclient import TestClient


import pytest

from ..apps import app
import crud
import models



@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

def test_db_insert_and_get_article(session):
    session = session
    # fixture = {'id': 1, 'contents': 'hello', 'writer': 'test@test.com', 'title': 'test-title'}
    # article = models.FreeBoard(**fixture)
    # crud.create_article(session, article)
    # article = crud.get_article(db=session, article_num=1)
    # assert article.id == fixture['id'] and article.contents == fixture['contents'] and \
    #        article.writer == fixture['writer'] and article.title == fixture['title']


def test_db_inset_and_get_comment(session):
    session = session
    # fixture = {'id': 1, 'contents': 'hello', 'writer': 'test@test.com', 'article_id': 1}
    # comment = models.Comment(**fixture)
    # crud.create_comment(session, comment)
    # comment = crud.get_comment(db=session, comment_id=1)
    # assert comment.id == fixture['id'] and comment.contents == fixture['contents'] and \
    #        comment.writer == fixture['writer']


# def test_api_article(session, client):
#     data = {'title': 'hello', 'contents': 'hello'}
#     res = client.post('/freeboard/write/article', json=data)
#     assert res.status_code == 201
#     res = client.get('/freeboard/2')
#     res_json = res.json()
#     assert res_json['title'] == data['title'] and res_json['contents'] == data['contents']
