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
else:
    BASE_DB_URL = 'mysql+pymysql://{USER}:{PASSWORD}@{ADDR}:{PORT}/{NAME}?charset=utf8'.format(
        USER="root",
        PASSWORD="rootpw", #read_secret("bakery-dev-db-password")
        ADDR="localhost", #34.64.195.33 / 127.0.0.1
        PORT=3306,
        NAME="flask-db" #bakery
    )

# else:
#     BASE_DB_URL = 'mysql+pymysql://{USER}:{PASSWORD}@{ADDR}:{PORT}/{NAME}?charset=utf8'.format(
#         USER="root",
#         PASSWORD=read_secret("bakery-dev-db-password"),
#         ADDR="34.64.195.33",
#         PORT=3306,
#         NAME="bakery"
#     )

print("test = {}".format(BASE_DB_URL))

base_engine = create_engine(BASE_DB_URL, echo=True)
