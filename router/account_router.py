from fastapi import APIRouter, Cookie, Depends
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

@router.post("/logout")
def login(accountService: AccountService = Depends()):
    return accountService.logout()

@router.get("/info")
def get_login_info(login_token: str | None = Cookie(default=None), accountService: AccountService = Depends()):
    return accountService.get_login_info(login_token)
