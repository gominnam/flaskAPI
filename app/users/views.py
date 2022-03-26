from flask.views import MethodView
from flask import jsonify, request
from app.users.services import get_user_name


class HelloWorld(MethodView):
    def get(self):
        name = get_user_name(request.args.get('id'))
        return jsonify({"username": name})


class myInfo(MethodView):
    def get(self):
        return jsonify({"name": "minjun", "gender": "m"})