from sqlalchemy import select
from sqlalchemy.orm import Session
from model.tables import Account
from utils.tokener import create_pretoken
from utils.mail import send_mail
from dotenv import load_dotenv
import os
import re

load_dotenv()

SERVICE_ADDRESS = os.getenv("SERVICE_ADDRESS")
EMAIL_FORMAT = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def verify_email_format(email: str) -> bool:
    return not EMAIL_FORMAT.fullmatch(email) is None

def check_email_register_status(email: str, db: Session) -> bool:
    statement = select(Account).where(Account.email == email)
    return not db.execute(statement).scalar_one_or_none() is None

def send_auth_mail(email: str, expire: int = 300) -> None:
    token = create_pretoken(email, expire)
    send_mail(
        To=email,
        Message=f"{SERVICE_ADDRESS}/signup?pretoken={token}"
    )