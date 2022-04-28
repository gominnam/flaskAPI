import datetime
import uuid

import requests
import responses
from flask_jwt_extended import create_access_token

from app.common import status
from app.users.services import generate_verification, join_user

join_data = {"phone_number": "01012345678",
             "user_id": "userId",
             "gender": "M",
             "birth": "19990909",
             "locale": "ko_KR.UTF-8",
             "token": ""}

join_sms_data = {"phone_number": "01012345678"}


def test_home(client):
    response = client.get('/users/home')
    assert response.status_code == status.HTTP_200_OK
    assert response.json == {"success": "Welcome Bakery"}


@responses.activate
def test_join_sms(client, mocker):
    mocker.patch("app.users.views.read_secret", return_value="ssi-bal")

    responses.add(responses.POST, 'https://sms.gabia.com/oauth/token', json={'access_token': 'test_token'}, status=200)
    resp = requests.post('https://sms.gabia.com/oauth/token')
    assert resp.json() == {'access_token': 'test_token'}

    responses.add(responses.POST, 'https://sms.gabia.com/api/send/sms', json={'error': 'not found'}, status=200)
    resp = requests.post('https://sms.gabia.com/api/send/sms')
    assert resp.json() == {'error': 'not found'}

    data = {
        'phone_number': '01011111111'
    }

    response = client.post('/users/join/sms', json=data)

    assert response.status_code == status.HTTP_200_OK


def insert_verification(phone_number, auth_code, token):
    created_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    auth_expired_time = str(datetime.datetime.strptime(created_time, '%Y-%m-%d %H:%M:%S')
                            + datetime.timedelta(minutes=3))
    join_expired_time = str(datetime.datetime.strptime(created_time, '%Y-%m-%d %H:%M:%S')
                            + datetime.timedelta(minutes=10))

    generate_verification(phone_number, auth_code, token, auth_expired_time, join_expired_time, created_time)


def test_join_auth(client):
    insert_verification('01012341234', '123456', 'token')

    data = {
        'phone_number': '01012341234',
        'auth_code': '123456'
    }

    response = client.post('/users/join/auth', json=data)

    assert response.status_code == status.HTTP_200_OK


def test_join(client):
    insert_verification('01012345678', '123456', 'token_asdf')

    data = {
        'phone_number': '01012345678',
        'user_id': 'test_user',
        'gender': 'W',
        'birth': '20220428',
        'locale': 'ko_KR.UTF-8',
        'token': 'token_asdf'
    }

    response = client.post('/users/join', json=data)

    assert response.status_code == status.HTTP_200_OK


def test_me(app, client):
    with app.app_context():
        join_user('01099999999', 'test_me', 'M', '20220429', 'ko_KR.UTF-8')

        access_token = create_access_token(identity={'phone_number': '01099999999'})
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }

        response = client.get('/users/me', headers=headers)

        assert response.status_code == status.HTTP_200_OK
