from fastapi import APIRouter, HTTPException, Depends
from service.CommentService import CommentService, CommentServiceException
from dto.CommentDto import CommentCreateRequestDto, CommentUpdateRequestDto, CommentResponseDto, CommentInternalDto
from utils.request_manager import get_log_in_token
from utils.crypto_manager import encode_id, decode_id
from utils.constant import NO_AUTHORITY

router = APIRouter(prefix="/comment", tags=["comment"])

@router.post("/{thingId:str}")
def create(request: CommentCreateRequestDto, thingId: str, logInToken = Depends(get_log_in_token), service: CommentService = Depends()):
    try:
        comment = service.create(request.content, decode_id(thingId), decode_id(logInToken["accountId"]))
    except CommentServiceException.NotFoundThing:
        raise HTTPException(status_code=404)
    
    response = internal_dto_to_response_dto(comment)
    return response

@router.get("/{thingId:str}")
def get_list(thingId: str, service: CommentService = Depends()):
    try:
        comments = service.get_list(decode_id(thingId))
    except CommentServiceException.NotFoundThing:
        raise HTTPException(status_code=404)
    response = [internal_dto_to_response_dto(comment) for comment in comments]
    return response

@router.put("/{commentId:str}")
def update(request: CommentUpdateRequestDto, commentId: str, logInToken: dict = Depends(get_log_in_token), service: CommentService = Depends()):
    try:
        comment = service.update(decode_id(commentId), decode_id(logInToken["accountId"]), request.content)
    except CommentServiceException.NoAuthority:
        raise HTTPException(status_code=403, detail=NO_AUTHORITY)
    except CommentServiceException.NotFoundComment:
        raise HTTPException(status_code=404)
    
    return internal_dto_to_response_dto(comment)

def internal_dto_to_response_dto(comment: CommentInternalDto) -> CommentResponseDto:
    comment.commentId = encode_id(comment.commentId)
    comment.createrId = encode_id(comment.createrId)
    return CommentResponseDto(**comment.model_dump())
