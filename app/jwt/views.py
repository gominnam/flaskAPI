from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_restx import Namespace, Resource

from app.common import status

jwt_app = Blueprint('jwt_app', __name__, url_prefix='/jwt')
jwt_api = Namespace('jwt_api', path='/jwt')


@jwt_api.route('/protected')
class protected(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), status.HTTP_200_OK


@jwt_api.route('/refresh')
class refresh(Resource):
    @jwt_required(refresh=True)
    def get(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return jsonify(access_token=access_token, current_user=current_user)
