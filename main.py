from flask import Flask
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

app = Flask(__name__)

app.add_url_rule("/", view_func=view.home.as_view('home'))
app.add_url_rule("/login", view_func=view.login.as_view('login'))
app.add_url_rule("/join", view_func=view.join.as_view('join'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
