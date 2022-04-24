from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_restx import Namespace, Resource

from app.common import status

token_app = Blueprint('token_app', __name__, url_prefix='/token')
token_api = Namespace('token_api', path='/token')


@token_api.route('/protected')
@token_api.header('Authorization: Bearer', 'JWT ACCESS TOKEN', required=True)
class protected(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {"logged_in_as": current_user}, status.HTTP_200_OK


@token_api.route('/refresh')
@token_api.header('Authorization: Bearer', 'JWT REFRESH TOKEN', required=True)
class refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {"access_token": access_token, "current_user": current_user}, status.HTTP_200_OK
