from sqlalchemy.orm import Session
from settings.db import base_engine
from app.users.models import User


def get_user_name(user_id):
    with Session(base_engine) as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
          return user.name
        else:
          return None