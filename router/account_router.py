from fastapi import APIRouter, Depends
from service.account_service import AccountService
from model.account_model import PreregisterRequest

router = APIRouter(prefix="/auth", tags=["/auth"])

@router.post("/preregister")
def preregister(preregisterRequest: PreregisterRequest, accountService: AccountService = Depends()):
    return accountService.preregister(preregisterRequest.email)