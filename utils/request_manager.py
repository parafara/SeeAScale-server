from fastapi import HTTPException, Form, Cookie
from utils.crypto_manager import verify_token
from dto.ThingDto import ThingCreateRequestDto, ThingUpdateRequestDto
from utils.constant import COOKIE_LOG_IN
from decimal import Decimal

class RequestManagerException:
    class NotLoggedIn(Exception): pass

def get_log_in_token(logInToken: str | None = Cookie(None, alias=COOKIE_LOG_IN)) -> dict | None:
    if logInToken is None: return None
    return verify_token(logInToken)
