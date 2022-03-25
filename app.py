from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import users.views as view

db_uri = 'mysql+pymysql://{USER}:{PASSWORD}@{ADDR}:{PORT}/{NAME}?charset=utf8'.format(
    USER="root",
    PASSWORD="rootpw",
    ADDR="localhost",
    PORT=3306,
    NAME="flask-db"
)


def discover_models():
    from users import models


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    db = SQLAlchemy(app)
    Migrate(app, db)

    discover_models()

    return app


app = create_app()

app.add_url_rule("/hello", view_func=view.HelloWorld.as_view('hello'))
app.add_url_rule("/myinfo", view_func=view.myInfo.as_view('myinfo'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
