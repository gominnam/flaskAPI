import os
import sqlalchemy
from sqlalchemy import create_engine
from settings.secrets import read_secret

ENV = os.environ.get('ENV', 'devel')

if ENV == 'prod':
    BASE_DB_URL = sqlalchemy.engine.url.URL(
        drivername="mysql+pymysql",
        username="root",
        password=read_secret("bakery-dev-db-password"),
        database="bakery",
        query={"unix_socket": "/cloudsql/{}".format("dunkinguys:asia-northeast3:muffin-dev")}
    )
elif ENV == 'test':
    BASE_DB_URL = 'mysql+pymysql://{USER}:{PASSWORD}@{ADDR}:{PORT}/{NAME}?charset=utf8'.format(
        USER="root",
        PASSWORD="rootpw",
        ADDR="localhost",
        PORT=3306,
        NAME="bakery-test"
    )
else:
    BASE_DB_URL = 'mysql+pymysql://{USER}:{PASSWORD}@{ADDR}:{PORT}/{NAME}?charset=utf8'.format(
        USER="root",
        PASSWORD="rootpw",
        ADDR="localhost",
        PORT=3306,
        NAME="bakery-dev"
    )

base_engine = create_engine(BASE_DB_URL, echo=True)
