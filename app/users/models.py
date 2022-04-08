from sqlalchemy import Column, Integer, String
from app.common.models import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String(128))
    password = Column(String(128))
    locale = Column(String(128))

    def __init__(self, phone_number, password, locale):
        self.phone_number = phone_number
        self.password = password
        self.locale = locale


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True, autoincrement=True)
