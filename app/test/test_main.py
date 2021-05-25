from fastapi.testclient import TestClient

from .. import urls
from ..apps import app


client = TestClient(app)


def test_main():
    response = client.get("/")
    assert response.status_code == 200


def test_get_quiz_path_only_hiragana():
    payload = {'kind': 'hiragana'}
    response = client.get(urls.inf_quiz_data_url, params=payload)
    json = response.json()
    assert json['path'].split('/')[3] == 'hiragana'


def test_get_quiz_path_only_katakana():
    payload = {'kind': 'katakana'}
    response = client.get(urls.inf_quiz_data_url, params=payload)
    json = response.json()
    assert json['path'].split('/')[3] == 'katakana'
