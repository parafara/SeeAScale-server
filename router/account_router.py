from fastapi import APIRouter, Depends
from service.account_service import AccountService
from model.account_model import PreregisterRequest, AccountCreateRequest, LoginRequest

router = APIRouter(prefix="/auth", tags=["/auth"])

@router.post("/preregister")
def preregister(request: PreregisterRequest, accountService: AccountService = Depends()):
    return accountService.preregister(request.email)

@router.get("/preverify")
def verify_pretoken(pretoken: str, accountService: AccountService = Depends()):
    return accountService.verify_pretoken(pretoken)

@router.post("/register")
def create_account(request: AccountCreateRequest, accountService: AccountService = Depends()):
    return accountService.create_account(request)

@router.post("/login")
def login(request: LoginRequest, accountService: AccountService = Depends()):
    return accountService.login(request)