def test_get_scoreboard_data(client, create_score):
    """
    스코어보드 데이터 요청 테스트
    """
    token = create_score
    header = {'Authorization': f'Bearer {token}'}
    response = client.get('/scoreboard/data', headers=header)
    json = response.json()
    assert response.status_code == 200
    assert len(json) == 2
    assert json.get("hiragana") and json.get("katakana")


def test_update_scoreboard_data(client, create_score):
    """
    스코어보드 데이터 업데이트 테스트
    """
    token = create_score
    header = {'Authorization': f'Bearer {token}'}
    body = dict(character="katakana/ka.png", quiz_type="katakana")
    response = client.patch('/scoreboard/data', json=body, headers=header)
    assert response.status_code == 204
    response = client.get('/scoreboard/data', headers=header)
    json = response.json()
    assert response.status_code == 200
    assert json.get("hiragana") and json.get("katakana")
    assert json.get("katakana").get("ka") == 1
