import jwt
from jwt import InvalidSignatureError, ExpiredSignatureError
import time
from dotenv import load_dotenv
import os

load_dotenv()

JWT_KEY = os.getenv("JWT_KEY")

def create_pretoken(email: str, expire: int) -> str:
    payload = {
        "email": email,
        "exp": int(time.time()) + expire
    }
    return jwt.encode(payload=payload, key=JWT_KEY, algorithm="HS256")

def verify_token(pretoken: str) -> dict | list:
    return jwt.decode(pretoken, JWT_KEY, "HS256")

def create_login_token(user_name: str, expire: int) -> str:
    payload = {
        "user_name": user_name,
        "exp": int(time.time()) + expire
    }
    return jwt.encode(payload=payload, key=JWT_KEY, algorithm="HS256")