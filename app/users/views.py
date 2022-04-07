from flask.views import MethodView
from flask import request, jsonify
from app.users.services import *


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


class home(MethodView):
    def get(self):
        return "Welcome Bakery"


class join(MethodView):
    def post(self):
        data = request.json
        phone_number = data.get('phone_number')
        password = data.get('password')
        locale = data.get('locale')

        if phone_number is None:
            return jsonify({"error": "phone_number_is_not_null"})
        elif password is None:
            return jsonify({"error": "password_is_not_null"})
        elif locale is None:
            return jsonify({"error": "locale_is_not_null"})

        return jsonify(post_user_join(phone_number, password, locale))
