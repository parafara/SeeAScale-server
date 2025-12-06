from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from decimal import Decimal
from utils.constant import NAME_FORMAT

class ThingCreateRequestDto(BaseModel):
    title: str
    prefix: int
    quantity: Decimal
    explanation: str

class ThingUpdateRequestDto(BaseModel):
    title: str | None
    prefix: int | None
    quantity: Decimal | None
    explanation: str | None

class ThingResponseDto(BaseModel):
    thingId: str
    title: str
    prefix: int
    quantity: Decimal
    explanation: str
    likesCount: int
    commentCount: int
    createdAt: datetime
    modifiedAt: datetime
    createrId: str
    createrName: str

class ThingInternalDto(BaseModel):
    thingId: int
    title: str
    prefix: int
    quantity: Decimal
    explanation: str
    likesCount: int
    commentCount: int
    createdAt: datetime
    modifiedAt: datetime
    createrId: int
    createrName: str | None = Field(None)

    model_config = ConfigDict(from_attributes=True, extra="ignore")
