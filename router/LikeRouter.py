from fastapi import APIRouter, Response, HTTPException, Depends
from service.LikeService import LikeService
from utils.request_manager import get_log_in_token
from utils.crypto_manager import decode_id


router = APIRouter(prefix="/like", tags=["like"])

@router.post("")
def create(thingId: str, logInToken = Depends(get_log_in_token), service: LikeService = Depends()):
    service.create(decode_id(thingId), decode_id(logInToken["accountId"]))

    return {}

@router.delete("")
def delete(thingId: str, logInToken = Depends(get_log_in_token), service: LikeService = Depends()):
    service.delete(decode_id(thingId), decode_id(logInToken["accountId"]))

    return {}

