from pydantic import BaseModel

class PreregisterRequest(BaseModel):
    email: str

class AccountCreateRequest(BaseModel):
    pretoken: str
    userName: str
    password: str

class LoginRequest(BaseModel):
    userEmail: str
    password: str