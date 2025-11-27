from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from utils.constant import THING_NAME_FORMAT

class ThingCreateRequest(BaseModel):
    thingName: str = Field(pattern=THING_NAME_FORMAT)
    prefix: int = Field(ge=-10, le=10)
    quantity: Decimal
    explaination: str = Field(min_length=0, max_length=500)

class ThingModifyRequest(BaseModel):
    thingName: str | None = Field(default=None, pattern=THING_NAME_FORMAT, examples=["물체이름"])
    prefix: int | None = Field(default=None, ge=-10, le=10, examples=[0])
    quantity: Decimal | None = Field(default=None, examples=["1.5"])
    explaination: str | None = Field(default=None, min_length=0, max_length=500, examples=["설명"])

class ThingSummaryResponse(BaseModel):
    thingId: str
    thingName: str
    prefix: int
    quantity: str
    likesCount: int
    commentCount: int
    createdAt: datetime
    modifiedAt: datetime
    createrId: str
    createrName: str

class ThingResponse(ThingSummaryResponse):
    explanation: str