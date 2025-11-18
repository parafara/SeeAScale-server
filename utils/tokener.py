import jwt
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
