from pydantic import BaseModel

class PreRegisterDTO(BaseModel):
    email: str

class RegisterDTO(BaseModel):
    pretoken: str
    user_name: str
    password: str

class LoginDTO(BaseModel):
    email: str
    password: str