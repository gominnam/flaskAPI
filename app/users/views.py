from flask import request, jsonify, Blueprint
from flask_restx import Resource, Namespace, reqparse

from app.common import status
from app.users.services import login_user, join_user


users_app = Blueprint('users_app', __name__, url_prefix='/api')
users_api = Namespace('users_api', path='/api')


@users_api.route('/home')
class home(Resource):
    def get(self):
        return {"success": "Welcome Bakery"}, status.HTTP_200_OK


login_parser = reqparse.RequestParser()
login_parser.add_argument('phone_number', location='json', type=str, help='휴대폰번호')
login_parser.add_argument('password', location='json', type=str,  help='비밀번호')


@users_api.route('/login')
class login(Resource):
    @users_api.expect(login_parser)
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


join_parser = reqparse.RequestParser()
join_parser.add_argument('phone_number', location='json', type=str, help='휴대폰번호')
join_parser.add_argument('password', location='json', type=str,  help='비밀번호')
join_parser.add_argument('locale', location='json', type=str,  help='lacale')


@users_api.route('/join')
class join(Resource):
    @users_api.expect(join_parser)
    def post(self):
        data = request.json
        phone_number = data.get('phone_number')
        password = data.get('password')
        locale = data.get('locale')

        if phone_number is None:
            return {"error": "phone_number_is_not_null"}, status.HTTP_400_BAD_REQUEST
        elif password is None:
            return {"error": "password_is_not_null"}, status.HTTP_400_BAD_REQUEST
        elif locale is None:
            return {"error": "locale_is_not_null"}, status.HTTP_400_BAD_REQUEST

        data, code = join_user(phone_number, password, locale)
        return data, code

