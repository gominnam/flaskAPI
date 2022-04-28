import requests
import responses

from app.common import status


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
