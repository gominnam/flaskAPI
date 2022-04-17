from app.common import status

join_data = {"phone_number": "01012345678",
             "password": "123456",
             "locale": "ko_KR.UTF-8"}

login_data = {"phone_number": "01012345678",
              "password": "123456"}


def test_home(client):
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json == {"success": "Welcome Bakery"}


def test_join_user(client):
    response = client.post('/join', json=join_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json == {"success": "welcome_slender"}


def test_login(client):
    response = client.post('/login', json=login_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json == {'name': join_data.get('phone_number')}


def test_login_with_invalid_phone(client):
    invalid_login_data = dict(login_data)
    invalid_login_data['password'] = '456123'
    response = client.post('/login', json=invalid_login_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
