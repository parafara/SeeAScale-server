from pydantic import BaseModel

class PreregisterRequest(BaseModel):
    email: str
