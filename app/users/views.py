import datetime
import uuid

import requests
from flask import request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace, fields

from app.common import status
from app.users.services import login_user, join_user, generate_verification, compare_created_time, complete_auth, \
    confirm_join_token, get_me, user_id_is_exist
from settings.secrets import read_secret

import base64
from random import randrange

users_app = Blueprint('users_app', __name__, url_prefix='/users')
users_api = Namespace('users_api', path='/users')


@users_api.route('/home')
class home(Resource):
    def get(self):
        return {"success": "Welcome Bakery"}, status.HTTP_200_OK


parser = users_api.parser()
parser.add_argument('Authorization', type=str, location='headers', help='Bearer access_token', required=True)


@users_api.route('/login')
@users_api.expect(parser)
class login(Resource):
    @jwt_required()
    def get(self):
        jwt_identity = get_jwt_identity()
        phone_number = jwt_identity['phone_number']

        data, status_code = login_user(phone_number)
        return data, status_code


join_model = users_api.model('join', {
    'phone_number': fields.String(required=True, description='휴대폰번호'),
    'user_id': fields.String(required=True, description='아이디'),
    'gender': fields.String(required=True, description='성별'),
    'birth': fields.String(required=True, description='생년월일'),
    'locale': fields.String(required=False, description='locale'),
    'token': fields.String(required=True, description='가입인증번호')
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
        token = data.get('token')

        if phone_number is None:
            return {"ok": False, "error": {"code": "phone_number_is_not_null", "message": "전화번호는 필수값 입니다."}}, status.HTTP_400_BAD_REQUEST
        elif user_id is None:
            return {"ok": False, "error": {"code": "user_id_is_not_null", "message": "유저아이디는 필수값 입니다."}}, status.HTTP_400_BAD_REQUEST
        elif gender is None:
            return {"ok": False, "error": {"code": "gender_is_not_null", "message": "성별은 필수값 입니다."}}, status.HTTP_400_BAD_REQUEST
        elif birth is None:
            return {"ok": False, "error": {"code": "birth_is_not_null", "message": "생년월일은 필수값 입니다."}}, status.HTTP_400_BAD_REQUEST
        elif token is None:
            return {"ok": False, "error": {"code": "token_is_not_null", "message": "토큰은 필수값 입니다."}}, status.HTTP_400_BAD_REQUEST

        request_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data, code = confirm_join_token(phone_number, token, request_time)

        if not data.get('ok'):
            return data, code

        data, code = join_user(phone_number, user_id, gender, birth, locale)
        return data, code


sms_model = users_api.model('sms', {
    'phone_number': fields.String(required=True, description='휴대폰번호')
})


@users_api.route('/join/sms')
class sms(Resource):
    @users_api.expect(sms_model)
    def post(self):
        data = request.json
        phone_number = data.get('phone_number')

        if phone_number is None:
            return {"ok": False, "error": {"code": "phone_number_is_not_null", "message": "전화번호는 필수값 입니다."}}, status.HTTP_400_BAD_REQUEST

        cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        comparator_time = datetime.datetime.strptime(cur_time, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(seconds=10)
        is_request_too_fast = compare_created_time(phone_number, comparator_time)

        if is_request_too_fast:
            return {"ok": False, "error": {"code": "sms_request_too_fast",
                                             "message": "인증코드를 요청한지 10초가 경과하지 않았습니다."}}, status.HTTP_400_BAD_REQUEST

        try:
            gabia_api_key = base64.b64encode(read_secret("gabia-sms-api-key").encode('ascii')).decode('ascii')
            url = 'https://sms.gabia.com/oauth/token'
            payload = ('grant_type=client_credentials').encode('utf-8')
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic ' + gabia_api_key
            }
            # get gabia access token request
            response = requests.request('POST', url, headers=headers, data=payload, allow_redirects=False,
                                        timeout=None)

            if response.status_code == 400:
                return response.text, status.HTTP_400_BAD_REQUEST

            resp = response.json()
            access_token = 'dunkinguys:' + resp['access_token']
            access_token = base64.b64encode(access_token.encode('ascii')).decode('ascii')
            auth_code = str(randrange(100000, 1000000))
            callback = read_secret("gabia-callback-number")

            url = 'https://sms.gabia.com/api/send/sms'
            payload = ('phone=' + phone_number + '&callback=' + callback + '&message=[Slender] 인증번호는 ' + auth_code + ' 입니다.&refkey=refkey').encode("utf-8")
            headers = {
               'Content-Type': 'application/x-www-form-urlencoded',
               'Authorization': 'Basic ' + access_token
            }
            # send sms auth_code
            requests.request('POST', url, headers=headers, data=payload, allow_redirects=False,
                                               timeout=None)

        except Exception as e:
            return e, status.HTTP_400_BAD_REQUEST

        token = uuid.uuid4().hex
        created_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        auth_expired_time = str(datetime.datetime.strptime(created_time, '%Y-%m-%d %H:%M:%S')
                                + datetime.timedelta(minutes=3))
        join_expired_time = str(datetime.datetime.strptime(created_time, '%Y-%m-%d %H:%M:%S')
                                + datetime.timedelta(minutes=10))

        data, code = generate_verification(phone_number, auth_code, token, auth_expired_time
                                           , join_expired_time, created_time)

        return data, code


auth_code_model = users_api.model('auth_code', {
    'phone_number': fields.String(required=True, description='휴대폰번호'),
    'auth_code': fields.String(required=True, description='인증코드')
})


@users_api.route('/join/auth')
class auth(Resource):
    @users_api.expect(auth_code_model)
    def post(self):
        data = request.json
        phone_number = data.get('phone_number')
        auth_code = data.get('auth_code')

        if phone_number is None:
            return {"ok": False, "error": {"code": "phone_number_is_not_null",
                                           "message": "전화번호는 필수값 입니다."}}, status.HTTP_400_BAD_REQUEST
        elif auth_code is None:
            return {"ok": False, "error": {"code": "auth_code_is_not_null",
                                           "message": "인증코드는 필수값 입니다."}}, status.HTTP_400_BAD_REQUEST

        request_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data, code = complete_auth(phone_number, auth_code, request_time)

        return data, code


user_id_valid_model = users_api.model('user_id_valid', {
    'user_id': fields.String(required=True, description='아이디'),
})


@users_api.route('/join/id-valid')  #  아이디 영문 숫자 특수문자(. 또는 _)만 가능,
class auth(Resource):
    @users_api.expect(user_id_valid_model)
    def post(self):
        data = request.json
        user_id = data.get('user_id')
        form_checking_user_id = user_id.replace('_', '')
        form_checking_user_id = form_checking_user_id('.', '')

        if user_id is None:
            return {"ok": False, "error": {"code": "user_id_is_not_null",
                                           "message": "유저 아이디는 필수 입력값 입니다."}}, status.HTTP_400_BAD_REQUEST
        elif len(user_id) < 3 or len(user_id) > 20:
            return {"ok": False, "error": {"code": "user_id_length_is_unvalid",
                                           "message": "유저 아이디 길이는 3~20자리까지 유효합니다."}}, status.HTTP_400_BAD_REQUEST
        elif form_checking_user_id.isalnum() is False:
            return {"ok": False, "error": {"code": "user_id_form_unvalid",
                                           "message": "유저 아이디 형식은 영어, 숫자 및 특수문자('.', '_')만 입력가능 합니다."}}, status.HTTP_400_BAD_REQUEST

        if user_id_is_exist(user_id) is not None:
            return {"ok": True, "message": "회원가입이 가능한 아이디 입니다."}, status.HTTP_200_OK


        return user_id


@users_api.route('/me')
@users_api.expect(parser)
class me(Resource):
    @jwt_required()
    def get(self):
        jwt_identity = get_jwt_identity()
        phone_number = jwt_identity['phone_number']

        data, code = get_me(phone_number)

        return data, code
