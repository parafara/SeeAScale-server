from sqlalchemy import select
from sqlalchemy.orm import Session
from model.tables import Account
from utils.tokener import create_token, verify_token, InvalidSignatureError, ExpiredSignatureError
from utils.mail import send_mail
from utils.crypto_tools import password_hashing, account_hashing, account_unhashing
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
PRETOKEN_EXPIRE_PERIOD = int(os.getenv("PRETOKEN_EXPIRE_PERIOD"))

def verify_email_format(email: str) -> bool:
    return not EMAIL_FORMAT.fullmatch(email) is None

def check_email_register_status(email: str, db: Session) -> bool:
    statement = select(Account).where(Account.email == email)
    return not db.execute(statement).scalar_one_or_none() is None

def send_auth_mail(email: str) -> None:
    pretoken = create_pretoken(email)
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

    return create_login_token(account_hashing(new_account.user_id), new_account.user_name)

def get_account_by_email(email: str, db: Session) -> Account | None:
    statement = select(Account).where(Account.email == email)
    return db.execute(statement).scalar_one_or_none()

def check_account_password(account: Account, password: str) -> bool:
    return account.password_hash == password_hashing(password)

def create_pretoken(email: str) -> str:
    payload = {
        "email": email
    }
    
    return create_token(payload, PRETOKEN_EXPIRE_PERIOD)

def create_login_token(user_id: int, user_name: str) -> str:
    payload = {
        "user_id": account_hashing(user_id),
        "user_name": user_name,
    }

    return create_token(payload, LOGIN_EXPIRE_PERIOD)
