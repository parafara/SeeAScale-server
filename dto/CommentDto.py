from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class CommentCreateRequestDto(BaseModel):
    content: str = Field(min_length=0, max_length=200)

class CommentUpdateRequestDto(BaseModel):
    content: str = Field(min_length=0, max_length=200)

class CommentResponseDto(BaseModel):
    commentId: str
    content: str
    createdAt: datetime
    modifiedAt: datetime
    createrId: str
    createrName: str

    model_config = ConfigDict(extra="ignore")

class CommentInternalDto(BaseModel):
    commentId: int
    content: str
    createdAt: datetime
    modifiedAt: datetime
    createrId: int
    createrName: str | None = Field(default=None)

    model_config = ConfigDict(from_attributes=True, extra="ignore")
