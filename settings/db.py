import os
from sqlalchemy import create_engine


# BASE_DB_USER = os.getenv('DB_USER', '')
# BASE_DB_PASSWORD = os.getenv('DB_PWD', '')
# BASE_DB_ADDRESS = "34.64.195.33"
# BASE_DB_PORT = 3306
# BASE_DB_NAME = "bakery"
# BASE_DB_URL = 'mysql+pymysql://{USER}:{PASSWORD}@{ADDR}:{PORT}/{NAME}?charset=utf8'.format(
#     USER=BASE_DB_USER,
#     PASSWORD=BASE_DB_PASSWORD,
#     ADDR=BASE_DB_ADDRESS,
#     PORT=BASE_DB_PORT,
#     NAME=BASE_DB_NAME
# )

BASE_DB_URL = 'sqlite:///app.db'

base_engine = create_engine(BASE_DB_URL, echo=True)