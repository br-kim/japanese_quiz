def test_get_scoreboard_data(client, create_score):
    token = create_score
    header = {'Authorization': f'Bearer {token}'}
    response = client.get('/scoreboard/data', headers=header)
    json = response.json()
    assert response.status_code == 200
    assert len(json) == 2
    assert json.get("hiragana") and json.get("katakana")


def test_update_scoreboard_data(client, create_score):
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
