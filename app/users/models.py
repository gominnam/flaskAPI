from sqlalchemy import Column, Integer, String, func, Date, DateTime
from app.common.models import Base


class User(Base):
    __tablename__ = 'user'

    phone_number = Column(String(128), primary_key=True)
    user_id = Column(String(128), nullable=False)
    gender = Column(String(1), nullable=False)
    birth = Column(Date(), nullable=False)
    locale = Column(String(128), default='ko_KR.UTF-8')
    time_created = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, phone_number, user_id, gender, birth, locale):
        self.phone_number = phone_number
        self.user_id = user_id
        self.gender = gender
        self.birth = birth
        self.locale = locale

    def serialize(self):
        return {"phone_number": self.phone_number,
                "user_id": self.user_id,
                "gender": self.gender,
                "birth": str(self.birth)}


class Verification(Base):
    __tablename__ = 'verification'

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String(128), primary_key=True)
    auth_code = Column(String(6), nullable=False)
    token = Column(String(128), nullable=False)
    auth_expired_time = Column(DateTime(), nullable=False) # 3m
    join_expired_time = Column(DateTime(), nullable=False) # 10m
    created_time = Column(DateTime(), nullable=False)

    def __init__(self, phone_number, auth_code, token, auth_expired_time, join_expired_time, created_time):
        self.phone_number = phone_number
        self.auth_code = auth_code
        self.token = token
        self.auth_expired_time = auth_expired_time
        self.join_expired_time = join_expired_time
        self.created_time = created_time
