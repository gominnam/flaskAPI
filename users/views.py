from flask_restx import Resource

from app import api


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {"username": "hello"}
