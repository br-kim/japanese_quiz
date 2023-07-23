def test_get_quiz_path_only_hiragana(client):
    """
    랜덤 퀴즈 히라가나 데이터 요청 테스트
    """
    payload = {'kind': 'hiragana'}
    response = client.get('/quiz-data/random', params=payload)
    json = response.json()
    assert json['path'].split('/')[3] == 'hiragana'


def test_get_quiz_path_only_katakana(client):
    """
    랜덤 퀴즈 카타카나 데이터 요청 테스트
    """
    payload = {'kind': 'katakana'}
    response = client.get('/quiz-data/random', params=payload)
    json = response.json()
    assert json['path'].split('/')[3] == 'katakana'


def test_get_quiz_path_both(client):
    """
    랜덤 퀴즈 모든 글자 데이터 요청 테스트
    """
    payload = {'kind': 'all'}
    response = client.get('/quiz-data/random', params=payload)
    json = response.json()
    gana_type = json['path'].split('/')[3]
    assert gana_type in ['hiragana', "katakana"]


def test_get_test_mode_data(client, create_user):
    """
    테스트 모드 데이터 요청 테스트
    """
    token = create_user
    payload = {'kind': 'all'}
    header = {'Authorization': f'Bearer {token}'}
    response = client.get('/quiz-data/test-mode', headers=header, params=payload)
    json = response.json()
    assert len(json['order']) == 208


def test_get_test_mode_data_hiragana(client, create_user):
    """
    테스트 모드 히라가나 데이터 요청 테스트
    """
    token = create_user
    payload = {'kind': 'hiragana'}
    header = {'Authorization': f'Bearer {token}'}
    response = client.get('/quiz-data/test-mode', headers=header, params=payload)
    json = response.json()
    assert len(json['order']) == 104


def test_get_test_mode_data_katakana(client, create_user):
    """
    테스트 모드 카타카나 데이터 요청 테스트
    """
    token = create_user
    payload = {'kind': 'katakana'}
    header = {'Authorization': f'Bearer {token}'}
    response = client.get('/quiz-data/test-mode', headers=header, params=payload)
    json = response.json()
    assert len(json['order']) == 104
