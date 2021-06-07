from fastapi.testclient import TestClient

import pytest

from ..apps import app
import dependencies


@pytest.mark.skip(reason="for dependency override")
def test_check_user():
    return True


app.dependency_overrides[dependencies.check_user] = test_check_user

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
