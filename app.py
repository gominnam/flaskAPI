from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import users.views as view

db_uri = 'mysql+pymysql://{USER}:{PASSWORD}@{ADDR}:{PORT}/{NAME}?charset=utf8'.format(
    USER="root",
    PASSWORD="",
    ADDR="34.64.195.33",
    PORT=3306,
    NAME="bakery"
)


def discover_models():
    from users import models


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    db.init_app(app)
    Migrate(app, db)

    discover_models()

    return app


app = create_app()

app.add_url_rule("/hello", view_func=view.HelloWorld.as_view('hello'))
app.add_url_rule("/myinfo", view_func=view.myInfo.as_view('myinfo'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
