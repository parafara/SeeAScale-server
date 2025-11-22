from fastapi import APIRouter, Depends
from service.account_service import AccountService
from model.account_model import PreregisterRequest, AccountCreateRequest, LoginRequest
from utils.cookie_manager import get_login_token

router = APIRouter(prefix="/auth", tags=["/auth"])

@router.post("/preregister")
def preregister(request: PreregisterRequest, service: AccountService = Depends()):
    return service.preregister(request=request)

@router.get("/preverify")
def verify_pretoken(pretoken: str, service: AccountService = Depends()):
    return service.verify_pretoken(pretoken=pretoken)

@router.post("")
def create_account(request: AccountCreateRequest, service: AccountService = Depends()):
    return service.create_account(request=request)

@router.post("/login")
def login(request: LoginRequest, service: AccountService = Depends()):
    return service.login(request=request)

@router.post("/logout")
def logout(service: AccountService = Depends()):
    return service.logout()

@router.get("/info")
def get_login_info(login_token: dict = Depends(get_login_token), service: AccountService = Depends()):
    return service.get_logined_user_info(login_token=login_token)
