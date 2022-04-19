
import requests
from flask import request, Blueprint
from flask_restx import Resource, Namespace, fields

from app.common import status
from app.users.services import login_user, join_user
from settings.secrets import read_secret

import base64
from random import randrange

users_app = Blueprint('users_app', __name__, url_prefix='/api')
users_api = Namespace('users_api', path='/api')


@users_api.route('/home')
class home(Resource):
    def get(self):
        return {"success": "Welcome Bakery"}, status.HTTP_200_OK


login_model = users_api.model('login', {
    'phone_number': fields.String(required=True, description='휴대폰번호'),
    'password': fields.String(required=True, description='비밀번호'),
})


@users_api.route('/login')
class login(Resource):
    @users_api.expect(login_model)
    def post(self):
        data = request.json
        phone_number = data.get('phone_number')
        user_password = data.get('password')

        if phone_number is None:
            return {"error": "phone_number_is_not_null"}
        elif user_password is None:
            return {"error": "password_is_not_null"}

        data, status_code = login_user(phone_number, user_password)
        return data, status_code


join_model = users_api.model('join', {
    'phone_number': fields.String(required=True, description='휴대폰번호'),
    'user_id': fields.String(required=True, description='아이디'),
    'gender': fields.String(required=True, description='성별'),
    'birth': fields.String(required=True, description='생년월일'),
    'locale': fields.String(required=False, description='locale'),
})


@users_api.route('/join')
class join(Resource):
    @users_api.expect(join_model)
    def post(self):
        data = request.json
        phone_number = data.get('phone_number')
        user_id = data.get('user_id')
        gender = data.get('gender')
        birth = data.get('birth')
        locale = data.get('locale')

        if phone_number is None:
            return {"error": "phone_number_is_not_null"}, status.HTTP_400_BAD_REQUEST
        elif user_id is None:
            return {"error": "user_id_is_not_null"}, status.HTTP_400_BAD_REQUEST
        elif gender is None:
            return {"error": "gender_is_not_null"}, status.HTTP_400_BAD_REQUEST
        elif birth is None:
            return {"error": "birth_is_not_null"}, status.HTTP_400_BAD_REQUEST

        # TODO : adding verification_table token column  check logic

        data, code = join_user(phone_number, user_id, gender, birth, locale)
        return data, code


sms_model = users_api.model('sms', {
    'phone_number': fields.Integer(required=True, description='휴대폰번호')
})


@users_api.route('/join/sms')
class sms(Resource):
    @users_api.expect(sms_model)
    def post(self):
        data = request.json
        phone_number = data.get('phone_number')

        if phone_number is None:
            return {"error": "phone_number_is_not_null"}, status.HTTP_400_BAD_REQUEST

        try:
            gabia_api_key = base64.b64encode(read_secret("gabia-sms-api-key").encode('ascii')).decode('ascii')
            url = 'https://sms.gabia.com/oauth/token'
            payload = ('grant_type=client_credentials').encode('utf-8')
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic ' + gabia_api_key
            }
            response = requests.request('POST', url, headers=headers, data=payload, allow_redirects=False,
                                        timeout=None)

            if response.status_code == 400:
                return response.text, status.HTTP_400_BAD_REQUEST

            resp = response.json()
            access_token = 'dunkinguys:' + resp['access_token']
            access_token = base64.b64encode(access_token.encode('ascii')).decode('ascii')
            auth_code = str(randrange(100000, 1000000))

            url = 'https://sms.gabia.com/api/send/sms'
            payload = ('phone=' + phone_number + '&callback=01050041618&message=[Slender] 인증번호는 ' + auth_code + ' 입니다.&refkey=refkey').encode("utf-8")
            headers = {
               'Content-Type': 'application/x-www-form-urlencoded',
               'Authorization': 'Basic ' + access_token
            }
            response = requests.request('POST', url, headers=headers, data=payload, allow_redirects=False,
                                               timeout=None)

        except Exception as e:
            return e, status.HTTP_400_BAD_REQUEST


        # TODO : adding verification table insert and return expired_time

        return {"expired_time": "times"}, status.HTTP_200_OK

# TODO : adding api auth_complete -> checking nearest expired time if same -> return token value