from fastapi import APIRouter, UploadFile, Response, HTTPException, Depends, Form, File, Query, Path
from fastapi.responses import FileResponse
from service.ThingService import ThingService, ThingServiceException
from dto.ThingDto import ThingSummaryResponseDto, ThingResponseDto, ThingSummaryInternalDto, ThingInternalDto
from utils.crypto_manager import encode_id, decode_id
from utils.request_manager import RequestManagerException, get_log_in_token
from utils.constant import WRONG_IMAGE_FORMAT, NO_AUTHORITY, DECIMAL_FORMAT, IMAGE_STORAGE_PATH
from decimal import Decimal

router = APIRouter(prefix="/thing", tags=["thing"])

@router.post("", status_code=201)
async def create(
    title: str = Form(min_length=1, max_length=32, examples=["물체 이름"]),
    imageFile: UploadFile = File(),
    prefix: int = Form(ge=-10, le=10, examples=[0]),
    quantity: str = Form(pattern=DECIMAL_FORMAT, examples=[1.78]),
    explanation: str = Form(min_length=0, max_length=500, examples=["물체 설명"]),
    logInToken: dict | None = Depends(get_log_in_token),
    service: ThingService = Depends()
):
    if logInToken is None: raise RequestManagerException.NotLoggedIn()
    imageData = await imageFile.read()
    quantity = Decimal(quantity)
    createrId = decode_id(logInToken["accountId"])
    try: thing = service.create(title, imageData, prefix, quantity, explanation, createrId)
    except ThingServiceException.WrongImageFormat: raise HTTPException(status_code=409, detail=WRONG_IMAGE_FORMAT)
    return internal2response(thing)

@router.get("")
def get_list(
    prefix: int = Query(ge=-10, le=10, example=0),
    page: int = Query(ge=0, example=0),
    byAsc: bool = Query(default=True),
    service: ThingService = Depends()
):
    things = service.get_list(prefix, page, byAsc)
    return [internal2response(thing) for thing in things]

@router.get("/{thingId:str}")
def get(thingId: str, logInToken: dict | None = Depends(get_log_in_token), service: ThingService = Depends()):
    thingId = decode_id(thingId)
    if logInToken: accountId = decode_id(logInToken["accountId"])
    else: accountId = None
    thing = service.get(thingId, accountId)
    if thing is None: raise HTTPException(status_code=404)
    return internal2response(thing)

@router.get("{thingId:str}/image")
def get_image(thingId: str = Path()):
    thingId = decode_id(thingId)
    try:
        return FileResponse(
            path=f"{IMAGE_STORAGE_PATH}/{thingId}.jpeg",
            media_type="image/jpeg"
        )
    except: raise HTTPException(status_code=404)

@router.patch("/{thingId:str}")
async def update(
    thingId: str = Path(),
    title: str | None = Form(default=None, min_length=1, max_length=32, examples=["물체 이름"]),
    imageFile: UploadFile | None = File(default=None),
    prefix: int | None = Form(default=None, ge=-10, le=10, examples=[0]),
    quantity: str | None = Form(default=None, pattern=DECIMAL_FORMAT, examples=[1.78]),
    explanation: str | None = Form(default=None, in_length=0, max_length=500, examples=["물체 설명"]),
    logInToken: dict | None = Depends(get_log_in_token),
    service: ThingService = Depends()
):
    if logInToken is None: raise RequestManagerException.NotLoggedIn()
    thingId = decode_id(thingId)
    imageData = await imageFile.read() if imageFile else None
    quantity = Decimal(quantity) if quantity else None
    accountId = decode_id(logInToken["accountId"])
    try:
        thing = service.update(thingId, accountId, title, imageData, prefix, quantity, explanation)
    except ThingServiceException.NoAuthoiry: raise HTTPException(status_code=403, detail=NO_AUTHORITY)
    except ThingServiceException.NotFoundThing: raise HTTPException(status_code=404)
    except ThingServiceException.WrongImageFormat: raise HTTPException(status_code=409, detail=WRONG_IMAGE_FORMAT)
    return internal2response(thing)

@router.delete("{thingId:str}")
def delete(thingId: str = Path(), logInToken: dict = Depends(get_log_in_token), service: ThingService = Depends()):
    if logInToken is None: raise RequestManagerException.NotLoggedIn()
    thingId = decode_id(thingId)
    accountId = decode_id(logInToken["accountId"])
    try:
        service.delete(thingId, accountId)
    except ThingServiceException.NoAuthoiry: raise HTTPException(status_code=403, detail=NO_AUTHORITY)
    except ThingServiceException.NotFoundThing: raise HTTPException(status_code=404)
    return Response(status_code=200)

def internal2response(internal: ThingSummaryInternalDto | ThingInternalDto) -> ThingSummaryResponseDto | ThingResponseDto:
    model = internal.model_dump()
    model["thingId"] = encode_id(model["thingId"])
    model["createrId"] = encode_id(model["createrId"])
    if type(internal) is ThingSummaryInternalDto: return ThingSummaryResponseDto(**model)
    elif type(internal) is ThingInternalDto: return ThingResponseDto(**model)
