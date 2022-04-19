from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from sentry_sdk.integrations.flask import FlaskIntegration
from settings.secrets import read_secret
import os
import app.users.views as view
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
api = Api(app, version='1.0', title='API 문서', description='Swagger 문서', doc="/api-docs")

api.add_namespace(view.users_api)
CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
