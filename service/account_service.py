from fastapi import Response, HTTPException, Depends
from repository.account_repository import AccountRepository
from model.account_model import PreregisterRequest, AccountCreateRequest, LoginRequest, InfoResponse
from utils.constant import RELEASE, PREREGISTER_EXPIRY_PERIOD, LOGIN_EXPIRY_PERIOD
from utils.token_manager import create_token, verify_token
from utils.mail_manager import send_preregister_mail
from utils.crypto_manager import hash_password, encode_id
from utils.schema import Account

class AccountService:
    def __init__(self, repository: AccountRepository = Depends()):
        self.repository = repository

    def preregister(self, request: PreregisterRequest):
        userEmail = request.userEmail

        if not self.repository.get_account_by_userEmail(userEmail) is None:
            raise HTTPException(status_code=409, detail="ALREADY_REGISTERED_EMAIL")
        
        pretoken = create_token({"email": userEmail}, expire=PREREGISTER_EXPIRY_PERIOD)

        send_preregister_mail(userEmail, pretoken)

        return Response(status_code=200)
    
    def verify_pretoken(self, pretoken: str):
        verify_token(pretoken)
        return Response(status_code=200)

    def create_account(self, request: AccountCreateRequest):
        userEmail = verify_token(request.pretoken)["email"]
        
        if not self.repository.get_account_by_userEmail(userEmail) is None:
            raise HTTPException(status_code=409, detail="ALREADY_REGISTERED_EMAIL")
          
        account = self.repository.create_account(userName=request.userName, userEmail=userEmail, password=request.password)

        return self.login_response(account, status_code=201)

    def login(self, request: LoginRequest):
        account = self.repository.get_account_by_userEmail(request.userEmail)

        if account is None:
            raise HTTPException(status_code=401, detail="UNREGISTERED_EMAIL")
        
        if account.passwordHash != hash_password(request.password):
            raise HTTPException(status_code=401, detail="INCORRECT_PASSWORD")
        
        return self.login_response(account)
    
    def login_response(self, account: Account, status_code: int = 200):
        login_token = create_token(
            payload={"userId": encode_id(account.userId), "userName": account.userName},
            expire=LOGIN_EXPIRY_PERIOD
        )

        response = Response(status_code=status_code)
        response.set_cookie(
            key="login_token",
            value=login_token,
            max_age=LOGIN_EXPIRY_PERIOD,
            httponly=True,
            samesite="strict",
            secure=RELEASE
        )

        return response
    
    def logout(self):
        response = Response(status_code=200)
        response.delete_cookie(
            key="login_token",
            httponly=True,
            samesite="strict",
            secure=RELEASE
        )

        return response

    def get_logined_user_info(self, login_token: dict):
        response = InfoResponse(
            userId=login_token["userId"],
            userName=login_token["userName"]
        )
        return response
