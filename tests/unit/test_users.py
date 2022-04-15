import json


user = {"phone_number": "01012345678",
        "password": "123456",
        "locale": "ko_KR.UTF-8"}


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"success": "Welcome Bakery"}


def test_post_user_join(client):
    response = client.post('/join', data=json.dumps(user), content_type='application/json')
    assert response.status_code == 200
    assert response.json == {"success": "welcome_slender"}


def test_user_login(client):
    response = client.post('/login', data=json.dumps(user), content_type='application/json')
    assert response.status_code == 200
    assert response.json == [{'name': user.get('phone_number')}, 200]

