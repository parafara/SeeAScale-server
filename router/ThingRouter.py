from fastapi import APIRouter, UploadFile, Response, HTTPException, Depends, File
from service.ThingService import ThingService, ThingServiceException
from dto.ThingDto import ThingCreateRequestDto, ThingResponseDto
from utils.crypto_manager import encode_id, decode_id
from utils.request_manager import get_log_in_token, thing_create_body
from utils.constant import WRONG_IMAGE_FORMAT
from io import BytesIO

router = APIRouter(prefix="/thing", tags=["thing"])

@router.post("")
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

    response = ThingResponseDto(
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

    return response

@router.get("/{thingId:str}")
def get(thingId: str, service: ThingService = Depends()):
    thing = service.get(decode_id(thingId))
    if thing is None: raise HTTPException(status_code=404)

    response = ThingResponseDto(
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

    return response
