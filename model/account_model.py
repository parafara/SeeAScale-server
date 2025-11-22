from pydantic import BaseModel, Field
from utils.constant import EMAIL_FORMAT, USER_NAME_FORMAT, PASSWORD_FORMAT

class PreregisterRequest(BaseModel):
    userEmail: str = Field(pattern=EMAIL_FORMAT, examples=["example@gmail.com"])

class AccountCreateRequest(BaseModel):
    pretoken: str = Field(examples=["pretoken"])
    userName: str = Field(pattern=USER_NAME_FORMAT, examples=["홍길동"])
    password: str = Field(pattern=PASSWORD_FORMAT, examples=["password!1234"])

class LoginRequest(BaseModel):
    userEmail: str = Field(pattern=EMAIL_FORMAT, examples=["example@gmail.com"])
    password: str = Field(pattern=PASSWORD_FORMAT, examples=["password!1234"])

class InfoResponse(BaseModel):
    userId: str
    userName: str