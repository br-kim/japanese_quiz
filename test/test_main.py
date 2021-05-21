from fastapi.testclient import TestClient

import urls
from ..apps import app


client = TestClient(app)


def test_main():
    response = client.get("/")
    assert response.status_code == 200


def test_get_quiz_path_only_hiragana():
    payload = {'hiragana': 'hiragana'}
    response = client.get(urls.inf_quiz_data_url, params=payload)
    json = response.json()
    assert json['path'].split('/')[3] == 'hiragana'


def test_get_quiz_path_only_katakana():
    payload = {'katakana': 'katakana'}
    response = client.get(urls.inf_quiz_data_url, params=payload)
    json = response.json()
    assert json['path'].split('/')[3] == 'katakana'
