from flask.views import MethodView
from flask import request, jsonify
from app.common import status
from app.users.services import login_user, post_user_join


class home(MethodView):
    def get(self):
        return jsonify({"success": "Welcome Bakery"}), status.HTTP_200_OK


class login(MethodView):
    def post(self):
        data = request.json
        phone_number = data.get('phone_number')
        user_password = data.get('password')

        if phone_number is None:
            return jsonify({"error": "phone_number_is_not_null"})
        elif user_password is None:
            return jsonify({"error": "password_is_not_null"})

        return jsonify(login_user(phone_number, user_password))


class join(MethodView):
    def post(self):
        data = request.json
        phone_number = data.get('phone_number')
        password = data.get('password')
        locale = data.get('locale')

        if phone_number is None:
            return jsonify({"error": "phone_number_is_not_null"}), status.HTTP_400_BAD_REQUEST
        elif password is None:
            return jsonify({"error": "password_is_not_null"}), status.HTTP_400_BAD_REQUEST
        elif locale is None:
            return jsonify({"error": "locale_is_not_null"}), status.HTTP_400_BAD_REQUEST

        data, code = post_user_join(phone_number, password, locale)
        return jsonify(data), code

