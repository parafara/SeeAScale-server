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

class ThingSummaryResponseDto(BaseModel):
    thingId: str
    title: str
    prefix: int
    quantity: Decimal
    likesCount: int
    commentCount: int
    createdAt: datetime
    modifiedAt: datetime
    createrId: str
    createrName: str

class ThingResponseDto(ThingSummaryResponseDto):
    explanation: str
    mine: bool
    liked: bool

class ThingSummaryInternalDto(BaseModel):
    thingId: int | str
    title: str
    prefix: int
    quantity: Decimal
    likesCount: int
    commentCount: int
    createdAt: datetime
    modifiedAt: datetime
    createrId: int | str
    createrName: str | None = Field(None)

    model_config = ConfigDict(from_attributes=True, extra="ignore")

class ThingInternalDto(ThingSummaryInternalDto):
    explanation: str
    mine: bool
    liked: bool