from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api, Resource, Namespace
from flask_sqlalchemy import SQLAlchemy

db_uri = 'mysql+pymysql://{USER}:{PASSWORD}@{ADDR}:{PORT}/{NAME}?charset=utf8'.format(
    USER="root",
    PASSWORD="rootpw",
    ADDR="localhost",
    PORT=3306,
    NAME="test_db"
)

db = SQLAlchemy()


def discover_models():
    from users import models


def discover_views():
    from users import views


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

    db.init_app(app)
    Migrate(app, db)

    # importing the models to make sure they are known to Flask-Migrate
    discover_models()

    return app


app = create_app()
api = Api(app)

ns = Namespace("hello", ordered=True)
from users.views import HelloWorld
api.register_resource(ns, HelloWorld, '/hello', '/world')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
