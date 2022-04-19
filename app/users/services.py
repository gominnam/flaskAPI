import sentry_sdk
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from settings.db import base_engine
from app.users.models import User
from app.common import status
from settings.secrets import read_secret


def login_user(phone_number: str, user_password: str) -> tuple[dict, int]:
    with Session(base_engine) as session:
        user = session.query(User).filter(User.phone_number == phone_number).first()

        if not user:
            return {"error": "phone_number_not_exist"}, status.HTTP_400_BAD_REQUEST
        elif user.password == user_password:
            return {"name": user.phone_number}, status.HTTP_200_OK
        else:
            return {"error": "incorrect_password"}, status.HTTP_400_BAD_REQUEST


def join_user(phone_number: str, user_id: str, gender: str, birth: str, locale: str) -> tuple[dict, int]:
    with Session(base_engine) as session:
        try:
            user = User(phone_number, user_id, gender, birth, locale)
            session.add(user)
            session.commit()
        except IntegrityError:
            return {"error": "duplicate_phone_number"}, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            sentry_sdk.capture_exception(e)
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST

        return {"success": "join_success_welcome_slender"}, status.HTTP_200_OK


# def auth_message(phone_number: str) -> tuple[dict, int]:
#     with Session(base_engine) as session:
#         try:
#             read_secret("bakery-dev-db-password")
#             # do gabia message service
