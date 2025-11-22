from fastapi import Response, HTTPException, Depends
from repository.account_repository import AccountRepository
from model.account_model import AccountCreateRequest, LoginRequest
from schema import Account
from utils.tokener import create_token, verify_token, jwt
from utils.mail import send_preregister_mail
from utils.crypto_tools import hash_password, encode_id
from dotenv import load_dotenv
import os
import re

load_dotenv()

COOKIE_SECURE_OPTION = os.getenv("COOKIE_SECURE_OPTION", None)

EMAIL_FORMAT = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
USER_NAME_FORMAT = re.compile(r"^[가-힣A-Za-z0-9_]{2,16}$")
PASSWORD_FORMAT = re.compile(r"^[A-Za-z0-9!@#$-_.?]{8,}$")

class AccountService:
    def __init__(self, repository: AccountRepository = Depends()):
        self.repository = repository

    def preregister(self, email: str):
        if EMAIL_FORMAT.fullmatch(email) is None:
            raise HTTPException(status_code=400, detail="INVALID_EMAIL_FORMAT")
        
        if not self.repository.get_account_by_userEmail(email) is None:
            raise HTTPException(status_code=400, detail="ALREADY_REGISTERED_EMAIL")
        
        pretoken = create_token({"email": email}, expire=300) # 5분

        send_preregister_mail(email, pretoken)

        return Response(status_code=204)
    
    def verify_pretoken(self, pretoken: str):
        try:
            verify_token(pretoken)
        except jwt.InvalidSignatureError:
            raise HTTPException(status_code=401, detail="INVALID_TOKEN")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="EXPIRED_TOKEN")
        return Response(status_code=204)

    def create_account(self, request: AccountCreateRequest):
        try: 
            userEmail = verify_token(request.pretoken)["email"]
        except jwt.InvalidSignatureError:
            raise HTTPException(status_code=401, detail="INVALID_TOKEN")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="EXPIRED_TOKEN")
        
        if not self.repository.get_account_by_userEmail() is None:
            raise HTTPException(status_code=400, detail="ALREADY_REGISTERED_EMAIL")

        if USER_NAME_FORMAT.fullmatch(request.userName) is None:
            raise HTTPException(status_code=400, detail="INVALID_USER_NAME")
        
        if PASSWORD_FORMAT.fullmatch(request.password) is None:
            raise HTTPException(status_code=400, detail="INVALID_PASSWORD")
          
        account = self.repository.create_account(request.userName, userEmail, request.password)

        return self.login_response(account, status_code=201)

    def login(self, request: LoginRequest):
        account = self.repository.get_account_by_userEmail(request.userEmail)

        if account is None:
            raise HTTPException(status_code=400, detail="UNREGISTERED_EMAIL")
        
        if account.passwordHash != hash_password(request.password):
            raise HTTPException(status_code=400, detail="INCORRECT_PASSWORD")
        
        return self.login_response(account)
    
    def login_response(self, account: Account, status_code: int = 200):
        login_token = create_token(
            payload={
                "userId": encode_id(account.userId),
                "userName": account.userName
            },
            expire=86400 # 하루
        )
        
        response = Response(status_code=status_code)
        response.set_cookie(
            key="login_token",
            value=login_token,
            max_age=86400, # 하루
            httponly=True,
            samesite="strict",
            secure = not COOKIE_SECURE_OPTION is None
        )

        return response
    
    def logout(self):
        response = Response(status_code=204)
        response.delete_cookie(
            key="login_token",
            httponly=True,
            samesite="strict",
            secure = not COOKIE_SECURE_OPTION is None
        )

        return response

    def get_login_info(self, login_token: str | None):
        if login_token is None:
            raise HTTPException(status_code=401, detail="NOT_LOGINED")
        
        try:
            user_info = verify_token(login_token)
        except jwt.InvalidSignatureError:
            raise HTTPException(status_code=401, detail="INVALID_TOKEN")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="EXPIRED_TOKEN")
        
        return {"userId": user_info["userId"], "userName": user_info["userName"]}
