from pydantic import BaseModel, ConfigDict, Field
from utils.constant import EMAIL_FORMAT, NAME_FORMAT, PASSWORD_FORMAT

class AccountPreregisterRequestDto(BaseModel):
    email: str = Field(pattern=EMAIL_FORMAT, examples=["example@gmail.com"])
    name: str = Field(pattern=NAME_FORMAT, examples=["See_A_Scale"])
    password: str = Field(pattern=PASSWORD_FORMAT, examples=["password"])

class AccountCreateRequestDto(BaseModel):
    signUpToken: str

class AccountLoginRequestDto(BaseModel):
    email: str = Field(pattern=EMAIL_FORMAT, examples=["example@gmail.com"])
    password: str = Field(pattern=PASSWORD_FORMAT, examples=["password"])

class AccountInternalDto(BaseModel):
    accountId: int
    email: str
    name: str

    model_config = ConfigDict(from_attributes=True, extra="ignore")
