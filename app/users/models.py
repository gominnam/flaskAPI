from sqlalchemy import Column, Integer, String
from app.common.models import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    locale = Column(String(128))


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
