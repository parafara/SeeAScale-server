from hashlib import sha256
from hashids import Hashids
from dotenv import load_dotenv
import os

load_dotenv()

HASH_PAPPER = os.getenv("HASH_PAPPER").encode()
ACCOUNT_HASHID_SALT = os.getenv("ACCOUNT_HASHID_SALT")
OBJECT_HASHID_SALT = os.getenv("OBJECT_HASHID_SALT")

account_hashid = Hashids(ACCOUNT_HASHID_SALT, 16)
object_hashid = Hashids(OBJECT_HASHID_SALT, 24)

def password_hashing(password: str) -> bytes:
    first_hashing = sha256(password.encode()).digest()
    second_hashing = sha256(first_hashing + HASH_PAPPER).digest()
    return second_hashing

def account_hashing(user_id: int) -> str:
    return account_hashid.encode(user_id)

def account_unhashing(user_id: str) -> int:
    return account_hashid.decode(user_id)[0]

def object_hashing(object_id: int) -> str:
    return object_hashid.encode(object_id)

def object_unhashing(object_id: str) -> int:
    return object_hashid.decode(object_id)[0]
