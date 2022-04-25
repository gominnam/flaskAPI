from datetime import timedelta

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restx import Api
from sentry_sdk.integrations.flask import FlaskIntegration
from settings.secrets import read_secret
import os
import app.users.views as view
import app.jwt.views as jwt
import sentry_sdk
from app.common import status

ENV = os.environ.get('ENV', 'devel')

if ENV == "prod":
    sentry_sdk.init(
        dsn=read_secret("bakery-sentry-dsn-key"),
        integrations=[FlaskIntegration()]
    )

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

app.register_blueprint(view.users_app)
app.register_blueprint(jwt.token_app)
api = Api(app, version='1.0', title='API 문서', description='Swagger 문서', doc="/api-docs")

api.add_namespace(view.users_api)
api.add_namespace(jwt.token_api)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['JWT_SECRET_KEY'] = "super-secret"  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=15)
app.config['PROPAGATE_EXCEPTIONS'] = True

jwt = JWTManager(app)


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return jsonify(ok=False, message="access_token_is_expired"), status.HTTP_400_BAD_REQUEST


@jwt.invalid_token_loader
def my_invalid_token_loader(token_invalid_reason):
    return jsonify(ok=False, message="access_token_is_invalid"), status.HTTP_400_BAD_REQUEST


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
