from sqlalchemy import select
from sqlalchemy.orm import Session
from model.tables import Account
from utils.tokener import create_pretoken, verify_token, create_login_token, InvalidSignatureError, ExpiredSignatureError
from utils.mail import send_mail
from utils.crypto_tools import password_hashing
from dotenv import load_dotenv
import os
import re

load_dotenv()

SERVICE_ADDRESS = os.getenv("SERVICE_ADDRESS")
EMAIL_FORMAT = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
USER_NAME_FORMAT = re.compile(r"^[가-힣A-Za-z0-9_]+$")
# 대소문자, 숫자, !@#$%^&*-_+=;:'",.<>?/ 특문, 최소 8자 이상
PASSWORD_FORMAT = re.compile(r"^[A-Za-z0-9!@#$%^&*\-_+=;:\'\",.<>?/]{8,}$")
LOGIN_EXPIRE_PERIOD = int(os.getenv("LOGIN_EXPIRE_PERIOD"))

def verify_email_format(email: str) -> bool:
    return not EMAIL_FORMAT.fullmatch(email) is None

def check_email_register_status(email: str, db: Session) -> bool:
    statement = select(Account).where(Account.email == email)
    return not db.execute(statement).scalar_one_or_none() is None

def send_auth_mail(email: str, expire: int = 300) -> None:
    pretoken = create_pretoken(email, expire)
    send_mail(
        To=email,
        Message=f"{SERVICE_ADDRESS}/auth/preverify?pretoken={pretoken}"
    )

def verify_user_name_format(user_name: str) -> bool:
    return not USER_NAME_FORMAT.fullmatch(user_name) is None

def verify_password_format(password: str) -> bool:
    return not PASSWORD_FORMAT.fullmatch(password) is None

def register_user(email: str, user_name: str, password: str, db: Session) -> str:
    password_hash = password_hashing(password)
    new_account = Account(user_name=user_name, email=email, password_hash=password_hash)
    db.add(new_account)
    db.commit()

    return create_login_token(new_account.user_name, LOGIN_EXPIRE_PERIOD)

def get_account_by_email(email: str, db: Session) -> Account | None:
    statement = select(Account).where(Account.email == email)
    return db.execute(statement).scalar_one_or_none()

def check_account_password(account: Account, password: str) -> bool:
    return account.password_hash == password_hashing(password)