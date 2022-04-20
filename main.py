from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restx import Api
from sentry_sdk.integrations.flask import FlaskIntegration
from settings.secrets import read_secret
import os
import app.users.views as view
import app.jwt.jwt_token as jwt
import sentry_sdk

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
app.register_blueprint(jwt.jwt_app)
api = Api(app, version='1.0', title='API 문서', description='Swagger 문서', doc="/api-docs")

api.add_namespace(view.users_api)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['JWT_SECRET_KEY'] = "super-secret"  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=15)

jwt = JWTManager(app)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
