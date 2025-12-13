from fastapi import APIRouter, Response, HTTPException, Depends, Path
from service.CommentService import CommentService, CommentServiceException
from dto.CommentDto import CommentCreateRequestDto, CommentUpdateRequestDto, CommentResponseDto, CommentInternalDto
from utils.request_manager import RequestManagerException, get_log_in_token
from utils.crypto_manager import encode_id, decode_id
from utils.constant import NO_AUTHORITY

router = APIRouter(prefix="/comment", tags=["comment"])

@router.post("/{thingId:str}", status_code=201)
def create(
    request: CommentCreateRequestDto,
    thingId: str = Path(),
    logInToken: dict | None = Depends(get_log_in_token),
    service: CommentService = Depends()
):
    if logInToken is None: raise RequestManagerException.NotLoggedIn()
    thingId = decode_id(thingId)
    accountId = decode_id(logInToken["accountId"])
    try: comment = service.create(request.content, thingId, accountId)
    except CommentServiceException.NotFoundThing: raise HTTPException(status_code=404)
    return internal2response(comment)

@router.get("/{thingId:str}")
def get_list(thingId: str, service: CommentService = Depends()):
    try:
        comments = service.get_list(decode_id(thingId))
    except CommentServiceException.NotFoundThing:
        raise HTTPException(status_code=404)
    response = [internal2response(comment) for comment in comments]
    return response

@router.put("/{commentId:str}")
def update(request: CommentUpdateRequestDto, commentId: str, logInToken: dict | None = Depends(get_log_in_token), service: CommentService = Depends()):
    if logInToken is None: raise RequestManagerException.NotLoggedIn()
    try:
        comment = service.update(decode_id(commentId), decode_id(logInToken["accountId"]), request.content)
    except CommentServiceException.NoAuthority:
        raise HTTPException(status_code=403, detail=NO_AUTHORITY)
    except CommentServiceException.NotFoundComment:
        raise HTTPException(status_code=404)
    
    return internal2response(comment)

@router.delete("/{commentId:str}")
def delete(commentId: str, logInToken: dict | None = Depends(get_log_in_token), service: CommentService = Depends()):
    if logInToken is None: raise RequestManagerException.NotLoggedIn()
    try:
        service.delete(decode_id(commentId), decode_id(logInToken["accountId"]))
    except CommentServiceException.NoAuthority:
        raise HTTPException(status_code=403, detail=NO_AUTHORITY)
    except CommentServiceException.NotFoundComment:
        raise HTTPException(status_code=404)
    return Response(status_code=200)

def internal2response(comment: CommentInternalDto) -> CommentResponseDto:
    model = comment.model_dump()
    model["commentId"] = encode_id(model["commentId"])
    model["createrId"] = encode_id(model["createrId"])
    return CommentResponseDto(**model)
