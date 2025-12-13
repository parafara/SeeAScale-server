from fastapi import APIRouter, Response, HTTPException, Depends
from service.LikeService import LikeService, LikeServiceException
from utils.request_manager import RequestManagerException, get_log_in_token
from utils.crypto_manager import decode_id
from utils.constant import ALREADY_REGISTERED


router = APIRouter(prefix="/like", tags=["like"])

@router.post("")
def create(thingId: str, logInToken: dict | None = Depends(get_log_in_token), service: LikeService = Depends()):
    if logInToken is None: raise RequestManagerException.NotLoggedIn()
    thingId, accountId = decode_id(thingId), decode_id(logInToken["accountId"])
    try: service.create(thingId, accountId)
    except LikeServiceException.AlreadyLiked: raise HTTPException(status_code=409, detail=ALREADY_REGISTERED)
    return Response(status_code=201)

@router.delete("")
def delete(thingId: str, logInToken = Depends(get_log_in_token), service: LikeService = Depends()):
    if logInToken is None: raise RequestManagerException.NotLoggedIn()
    thingId, accountId = decode_id(thingId), decode_id(logInToken["accountId"])
    try: service.delete(thingId, accountId)
    except LikeServiceException.NotLiked: raise HTTPException(status_code=404)
    return Response(status_code=200)

