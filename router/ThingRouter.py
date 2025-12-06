from fastapi import APIRouter, UploadFile, HTTPException, Depends, File, Query
from service.ThingService import ThingService, ThingServiceException
from dto.ThingDto import ThingCreateRequestDto, ThingUpdateRequestDto, ThingResponseDto, ThingInternalDto
from utils.crypto_manager import encode_id, decode_id
from utils.request_manager import get_log_in_token, thing_create_body, thing_update_body
from utils.constant import WRONG_IMAGE_FORMAT, NO_AUTHORITY
from io import BytesIO

router = APIRouter(prefix="/thing", tags=["thing"])

@router.post("", status_code=201)
async def create(
    request: ThingCreateRequestDto = Depends(thing_create_body),
    imageFile: UploadFile = File(),
    logInToken: dict = Depends(get_log_in_token),
    service: ThingService = Depends()
):
    try:
        thing = service.create(
            request.title,
            BytesIO(await imageFile.read()),
            request.prefix,
            request.quantity,
            request.explanation,
            decode_id(logInToken["accountId"])
        )
    except ThingServiceException.WrongImageFormat:
        raise HTTPException(status_code=409, detail=WRONG_IMAGE_FORMAT)

    response = internal_dto_to_response_dto(thing)

    return response

@router.get("")
def get_list(prefix: int = Query(ge=-10, le=10), page: int = Query(ge=0), service: ThingService = Depends()):
    try:
        things = service.get_list(prefix, page)
    except ThingServiceException.NotFoundThing:
        raise HTTPException(status_code=404)

    response = [internal_dto_to_response_dto(thing) for thing in things]

    return response

@router.get("/{thingId:str}")
def get(thingId: str, service: ThingService = Depends()):
    thing = service.get(decode_id(thingId))
    if thing is None: raise HTTPException(status_code=404)

    response = internal_dto_to_response_dto(thing)

    return response

@router.patch("/{thingId:str}")
async def update(
    thingId: str,
    request: ThingUpdateRequestDto = Depends(thing_update_body),
    imageFile: UploadFile | None = File(default=None),
    logInToken: dict = Depends(get_log_in_token),
    service: ThingService = Depends()
):
    if imageFile: image = BytesIO(await imageFile.read())
    else: image = None
    try:
        thing = service.update(
            decode_id(thingId),
            decode_id(logInToken["accountId"]),
            request.title,
            image,
            request.prefix,
            request.quantity,
            request.explanation
        )
    except ThingServiceException.NoAuthoiry:
        raise HTTPException(status_code=403, detail=NO_AUTHORITY)
    except ThingServiceException.NotFoundThing:
        raise HTTPException(status_code=404)
    except ThingServiceException.WrongImageFormat:
        raise HTTPException(status_code=409, detail=WRONG_IMAGE_FORMAT)

    response = internal_dto_to_response_dto(thing)
    return response


def internal_dto_to_response_dto(thing: ThingInternalDto) -> ThingResponseDto:
    result = ThingResponseDto(
        thingId=encode_id(thing.thingId),
        title=thing.title,
        prefix=thing.prefix,
        quantity=thing.quantity,
        explanation=thing.explanation,
        likesCount=thing.likesCount,
        commentCount=thing.commentCount,
        createdAt=thing.createdAt,
        modifiedAt=thing.modifiedAt,
        createrId=encode_id(thing.createrId),
        createrName=thing.createrName,
    )
    return result
