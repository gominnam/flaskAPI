import sentry_sdk
from sqlalchemy.orm import Session
from settings.db import base_engine
from app.users.models import User
from app.common import status


def login_user(phone_number: str, user_password: str) -> tuple[dict, int]:
    with Session(base_engine) as session:
        user = session.query(User).filter(User.phone_number == phone_number).first()

        if not user:
            return {"error": "phone_number_not_exist"}, status.HTTP_400_BAD_REQUEST

        if user.password == user_password:
            return {"name": user.phone_number}, status.HTTP_200_OK
        else:
            return {"error": "incorrect_password"}, status.HTTP_400_BAD_REQUEST


def post_user_join(name: str, password: str, locale: str) -> tuple[dict, int]:
    with Session(base_engine) as session:
        try:
            user = User(name, password, locale)
            session.add(user)
            session.commit()
        except Exception as e:
            sentry_sdk.capture_exception(e)
            return {"error": e}, status.HTTP_400_BAD_REQUEST

        return {"success": "welcome_slender"}, status.HTTP_200_OK
