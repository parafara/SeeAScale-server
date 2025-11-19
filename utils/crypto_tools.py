from hashlib import sha256
from dotenv import load_dotenv
import os

load_dotenv()

HASH_PAPPER = os.getenv("HASH_PAPPER").encode()

def password_hashing(password: str) -> bytes:
    first_hashing = sha256(password.encode()).digest()
    second_hashing = sha256(first_hashing + HASH_PAPPER).digest()
    return second_hashing