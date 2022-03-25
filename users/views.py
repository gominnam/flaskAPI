from flask.views import MethodView
from flask import jsonify


class HelloWorld(MethodView):
    def get(self):
        return jsonify({"username": "hello"})


class myInfo(MethodView):
    def get(self):
        return jsonify({"name": "minjun", "gender": "m"})
