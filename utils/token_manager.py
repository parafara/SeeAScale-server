from fastapi import HTTPException
from utils.constant import JWT_KEY, JWT_ALGORITHM
from typing import Any
import jwt
import time

def create_token(payload: dict, expire: int) -> str:
    payload["exp"] = int(time.time()) + expire
    return jwt.encode(payload=payload, key=JWT_KEY, algorithm=JWT_ALGORITHM)

def verify_token(token: str) -> Any:
    try:
        return jwt.decode(token, JWT_KEY, JWT_ALGORITHM)
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=401, detail="INVALID_TOKEN")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="EXPIRED_TOKEN")
