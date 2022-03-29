from sqlalchemy import create_engine
from settings.secrets import read_secret

BASE_DB_URL = 'mysql+pymysql://{USER}:{PASSWORD}@{ADDR}:{PORT}/{NAME}?charset=utf8'.format(
    USER="root",
    PASSWORD=read_secret("bakery-dev-db-password"),
    ADDR="34.64.195.33",
    PORT=3306,
    NAME="bakery"
)

base_engine = create_engine(BASE_DB_URL, echo=True)