from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_restx import Namespace

from app.common import status


jwt_app = Blueprint('jwt_app', __name__, url_prefix='')
jwt_api = Namespace('jwt_api', path='')


@jwt_api.route('/protected')  # GET
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), status.HTTP_200_OK


@jwt_api.route('/refresh')  # GET
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token, current_user=current_user)