from hashlib import sha256
from hashids import Hashids
from utils.constant import HASH_PAPPER, HASH_ID_SALT

hashid = Hashids(HASH_ID_SALT, 16)

def hash_password(password: str) -> bytes:
    first_hashing = sha256(password.encode()).digest()
    second_hashing = sha256(first_hashing + HASH_PAPPER).digest()
    return second_hashing

def encode_id(id: int) -> str:
    return hashid.encode(id)

def decode_id(id: str) -> int:
    return hashid.decode(id)