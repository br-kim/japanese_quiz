from fastapi.testclient import TestClient

from ..apps import app
import dependencies


def check_user():
    return True


app.dependency_overrides[dependencies.check_user] = check_user

client = TestClient(app)


def test_get_quiz_path_only_hiragana():
    payload = {'kind': 'hiragana'}
    response = client.get('/quizdata/path', params=payload)
    json = response.json()
    assert json['path'].split('/')[3] == 'hiragana'


def test_get_quiz_path_only_katakana():
    payload = {'kind': 'katakana'}
    response = client.get('/quizdata/path', params=payload)
    json = response.json()
    assert json['path'].split('/')[3] == 'katakana'


def test_get_quiz_path_both():
    payload = {'kind': 'all'}
    response = client.get('/quizdata/path', params=payload)
    json = response.json()
    gana_type = json['path'].split('/')[3]
    assert gana_type == 'katakana' or gana_type == 'hiragana'
