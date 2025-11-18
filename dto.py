from pydantic import BaseModel

class PreRegisterDTO(BaseModel):
    email: str