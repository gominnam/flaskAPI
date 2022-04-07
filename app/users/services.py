from sqlalchemy.orm import Session
from settings.db import base_engine
from app.users.models import User


def get_user_name(user_id):
    with Session(base_engine) as session:
        user = session.query(User).filter(User.name == user_id).first()
        if user:
          return user.name
        else:
          return None


def login_user(phone_number: str, user_password: str) -> dict:
    with Session(base_engine) as session:
        user = session.query(User).filter(User.phone_number == phone_number).first()

        if not user:
            return {"error": "phone_number_not_exist"}

        if user.password == user_password:
            return {"name": user.phone_number}
        else:
            return {"error": "incorrect_password"}



def post_user_join(name, password, locale):
    with Session(base_engine) as session:
        try:
            user = User(name, password, locale)
            session.add(user)
            session.commit()
        except Exception as e:
            return {"error": e}

        return {"success": "welcome_slender"}
