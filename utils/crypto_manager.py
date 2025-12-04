from hashlib import sha256
from hashids import Hashids
import jwt
import time
from utils.constant import PASSWORD_HASHING_PAPPER, ID_HASHING_SALT, JWT_KEY, JWT_ALGORITHM

class CryptoManagerException:
    class InvalidId(Exception): pass
    class InvalidToken(Exception): pass
    class ExpiredToken(Exception): pass

hashid = Hashids(ID_HASHING_SALT, 16)

def hash_password(password: str) -> bytes:
    first_hashing = sha256(password.encode()).digest()
    second_hashing = sha256(first_hashing + PASSWORD_HASHING_PAPPER).digest()
    return second_hashing

def encode_id(id: int) -> str:
    return hashid.encode(id)

def decode_id(id: str) -> int:
    id = hashid.decode(id)
    if id == (): raise CryptoManagerException.InvalidId()
    return id[0]

def create_token(payload: dict, expire: int) -> str:
    payload["exp"] = int(time.time()) + expire
    return jwt.encode(payload=payload, key=JWT_KEY, algorithm=JWT_ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_KEY, JWT_ALGORITHM)
    except jwt.InvalidSignatureError:
        raise CryptoManagerException.InvalidToken()
    except jwt.ExpiredSignatureError:
        raise CryptoManagerException.ExpiredToken()
