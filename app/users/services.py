import datetime

import sentry_sdk
from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from settings.db import base_engine
from app.users.models import User, Verification
from app.common import status


def login_user(phone_number: str) -> tuple[dict, int]:
    with Session(base_engine) as session:
        user = session.query(User).filter(User.phone_number == phone_number).first()

        if not user:
            return {"ok": False, "error": {"code": "phone_number_not_exist"
                                        , "message": "가입하지 않은 번호 입니다."}}, status.HTTP_400_BAD_REQUEST

        access_token = create_access_token(identity={'phone_number': phone_number})
        refresh_token = create_refresh_token(identity={'phone_number': phone_number})
        return {"ok": True, "token": {"access_token": access_token, "refresh_token": refresh_token}}, status.HTTP_200_OK


def join_user(phone_number: str, user_id: str, gender: str, birth: str, locale: str) -> tuple[dict, int]:
    with Session(base_engine) as session:
        try:
            user = User(phone_number, user_id, gender, birth, locale)
            session.add(user)
            session.commit()
        except IntegrityError:
            return {"ok": False, "error": {"code": "duplicate_phone_number",
                                           "message": "이미 가입한 전화번호 입니다."}}, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            sentry_sdk.capture_exception(e)
            return {"ok": False, "error": str(e)}, status.HTTP_400_BAD_REQUEST

        access_token = create_access_token(identity={'phone_number': phone_number})
        refresh_token = create_refresh_token(identity={'phone_number': phone_number})
        return {"ok": True, "token": {"access_token": access_token, "refresh_token": refresh_token}}, status.HTTP_200_OK


def generate_verification(phone_number: str, auth_code: str, token: str, auth_expired_time: str
                          , join_expired_time: str, created_time: str) -> tuple[dict, int]:
    with Session(base_engine) as session:
        verification = Verification(phone_number, auth_code, token, auth_expired_time, join_expired_time, created_time)
        session.add(verification)
        session.commit()

        return {"ok": True, "auth_expired_time": auth_expired_time}, status.HTTP_200_OK


def compare_created_time(phone_number: str, comparator_time: datetime) -> bool:
    with Session(base_engine) as session:
        verification = session.query(Verification).filter(Verification.phone_number == phone_number,
                                                          Verification.created_time >= comparator_time) \
                                                    .order_by(desc(Verification.id)).first()
        if verification:
            return True
        else:
            return False


def complete_auth(phone_number: str, auth_code: str, request_time: str) -> tuple[dict, int]:
    with Session(base_engine) as session:
        verification = session.query(Verification).filter(Verification.phone_number == phone_number) \
                                                    .order_by(desc(Verification.id)).first()

        if datetime.datetime.strptime(request_time, '%Y-%m-%d %H:%M:%S') > verification.auth_expired_time:
            return {"ok": False, "error": {"code": "auth_expired_time_over"
                                            , "message": "인증 만료시간이 초과 했습니다."}}, status.HTTP_400_BAD_REQUEST
        elif auth_code != verification.auth_code:
            return {"ok": False, "error": {"code": "not_match_auth_code"
                                            , "message": "인증번호가 일치하지 않습니다."}}, status.HTTP_400_BAD_REQUEST

        return {"ok": True}, status.HTTP_200_OK


def confirm_join_token(phone_number: str, token: str, request_time: str) -> tuple[dict, int]:
    with Session(base_engine) as session:
        verification = session.query(Verification).filter(Verification.phone_number == phone_number) \
            .order_by(desc(Verification.id)).first()

        if datetime.datetime.strptime(request_time, '%Y-%m-%d %H:%M:%S') > verification.join_expired_time:
            return {"ok": False, "error": {"code": "join_expired_time_over"
                , "message": "인증 시간이 만료 했습니다."}}, status.HTTP_400_BAD_REQUEST
        elif token != verification.token:
            return {"ok": False, "error": {"code": "not_match_auth_code"
                , "message": "인증 토큰이 일치하지 않습니다."}}, status.HTTP_400_BAD_REQUEST

        return {"ok": True, "token": verification.token}, status.HTTP_200_OK


def get_me(phone_number: str) -> tuple[dict, int]:
    with Session(base_engine) as session:
        user = session.query(User).filter(User.phone_number == phone_number).first()

        if not user:
            return {"ok": False, "error": {"code": "can_not_found_user_info"
                                        , "message": "회원정보를 찾을 수 없습니다."}}, status.HTTP_400_BAD_REQUEST

        user_info = user.serialize()

        return {"ok": True, "user": user_info}, status.HTTP_200_OK
