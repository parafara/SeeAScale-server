import jwt
import time
from dotenv import load_dotenv
import os

load_dotenv()

JWT_KEY = os.getenv("JWT_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

def create_token(payload: dict, expire: int) -> str:
    payload["exp"] = int(time.time()) + expire
    return jwt.encode(payload=payload, key=JWT_KEY, algorithm=JWT_ALGORITHM)

def verify_token(token: str):
    return jwt.decode(token, JWT_KEY, JWT_ALGORITHM)
