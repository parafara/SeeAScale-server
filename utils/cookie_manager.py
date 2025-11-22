from fastapi import HTTPException, Cookie
from utils.token_manager import verify_token

def get_login_token(login_token: str | None = Cookie(None)) -> dict:
    if login_token is None:
        raise HTTPException(status_code=401, detail="NOT_LOGINED")
    return verify_token(login_token)