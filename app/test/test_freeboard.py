import crud
import models


def test_get_article_list(client, create_article_fixture):
    """
    게시글 리스트 요청 테스트
    """
    res = client.get("/freeboard",params={'page':1})
    response = res.json()
    assert res.status_code == 200
    assert response.get("articles_length") == 1
    assert response.get("articles")[0].get("title") == "test"
    assert response.get("articles")[0].get("contents") == "test"


def test_write_article(client, session, create_user):
    """
    게시글 작성 테스트
    """
    header = {"Authorization": "Bearer " + create_user}
    res = client.post("/freeboard/write/article",headers=header, json={"title": "test", "contents": "test"})
    assert res.status_code == 201
    articles = session.query(models.FreeBoard).all()
    assert res.json() == articles[0].id


def test_write_comment(client, session, create_article_fixture):
    """
    댓글 작성 테스트
    """
    token, exist_article = create_article_fixture
    header = {"Authorization": "Bearer " + token}
    res = client.post("/freeboard/write/comment",headers=header, json={"article_id": exist_article.id, "contents": "test"})
    assert res.status_code == 201
    comments = session.query(models.Comment).all()
    assert res.json() == comments[0].id
    assert comments[0].contents == "test"


def test_edit_article(client, session, create_article_fixture):
    """
    게시글 수정 테스트
    """
    token, exist_article = create_article_fixture
    exist_article_id = exist_article.id
    body = dict(title="edited", contents="edited")
    header = {"Authorization": "Bearer " + token}
    res = client.patch(f"/freeboard/article/{exist_article_id}",headers=header, json=body)
    assert res.status_code == 204
    article = session.query(models.FreeBoard).filter(models.FreeBoard.id == exist_article_id).first()
    assert article.title == "edited"
    assert article.contents == "edited"

def test_edit_comment(client, session, create_comment_fixture):
    """
    댓글 수정 테스트
    """
    token, exist_comment = create_comment_fixture
    exist_comment_id = exist_comment.id
    body = dict(contents="edited")
    header = {"Authorization": "Bearer " + token}
    res = client.patch(f"/freeboard/comment/{exist_comment_id}",headers=header, json=body)
    assert res.status_code == 204
    comment = session.query(models.Comment).filter(models.Comment.id == exist_comment_id).first()
    assert comment.contents == "edited"

def test_delete_article(client, session, create_article_fixture):
    """
    게시글 삭제 테스트
    """
    token, exist_article = create_article_fixture
    exist_article_id = exist_article.id
    header = {"Authorization": "Bearer " + token}
    res = client.delete(f"/freeboard/article/{exist_article_id}",headers=header)
    assert res.status_code == 204
    article = session.query(models.FreeBoard).filter(models.FreeBoard.id == exist_article_id).first()
    assert article is None

def test_delete_comment(client, session, create_comment_fixture):
    """
    댓글 삭제 테스트
    """
    token, exist_comment = create_comment_fixture
    exist_comment_id = exist_comment.id
    header = {"Authorization": "Bearer " + token}
    res = client.delete(f"/freeboard/comment/{exist_comment_id}",headers=header)
    assert res.status_code == 204
    comment = session.query(models.Comment).filter(models.Comment.id == exist_comment_id).first()
    assert comment is None


def test_get_article(client, session, create_article_fixture):
    """
    게시글 요청 테스트
    """
    token, exist_article = create_article_fixture
    exist_article_id = exist_article.id
    header = {"Authorization": "Bearer " + token}
    res = client.get(f"/freeboard/{exist_article_id}", headers=header)
    assert res.status_code == 200
    assert res.json().get("title") == "test"
    assert res.json().get("contents") == "test"

def test_get_comment(client, session, create_comment_fixture):
    """
    댓글 요청 테스트
    """
    token, exist_comment = create_comment_fixture
    exist_comment_id = exist_comment.id
    header = {"Authorization": "Bearer " + token}
    res = client.get(f"/freeboard/comment/{exist_comment_id}", headers=header)
    assert res.status_code == 200
    assert res.json().get("contents") == "test"
