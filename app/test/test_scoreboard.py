def test_get_scoreboard_data(client, create_score):
    token = create_score
    header = {'Authorization': f'Bearer {token}'}
    response = client.get('/scoreboard/data', headers=header)
    json = response.json()
    assert response.status_code == 200
    assert len(json) == 2
    assert json.get("hiragana") and json.get("katakana")
