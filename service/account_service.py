from fastapi import Response, HTTPException, Depends
from repository.account_repository import AccountRepository
from model.account_model import AccountCreateRequest, LoginRequest
from utils.tokener import create_token, verify_token, jwt
from utils.mail import send_preregister_mail
from utils.crypto_tools import encode_id
from dotenv import load_dotenv
import os
import re

load_dotenv()

COOKIE_SECURE_OPTION = os.getenv("COOKIE_SECURE_OPTION", None)

EMAIL_FORMAT = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
USER_NAME_FORMAT = re.compile(r"^[가-힣A-Za-z0-9_]+$")
PASSWORD_FORMAT = re.compile(r"^[A-Za-z0-9!@#$-_.?]{8,}$")

class AccountService:
    def __init__(self, repository: AccountRepository = Depends()):
        self.repository = repository

    def preregister(self, email: str):
        if EMAIL_FORMAT.fullmatch(email) is None:
            raise HTTPException(status_code=400, detail="INVALID_EMAIL_FORMAT")
        
        if not self.repository.get_account_by_email(email) is None:
            raise HTTPException(status_code=400, detail="ALREADY_REGISTERED_EMAIL")
        
        pretoken = create_token({"email": email}, expire=300) # 5분

        send_preregister_mail(email, pretoken)

        return Response(status_code=200)
    
    def verify_pretoken(self, pretoken: str):
        try:
            verify_token(pretoken)
        except jwt.InvalidSignatureError:
            raise HTTPException(status_code=401, detail="INVALID_TOKEN")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="EXPIRED_TOKEN")
        return Response(status_code=200)

    def create_account(self, request: AccountCreateRequest):
        try: 
            userEmail = verify_token(request.pretoken)["email"]
        except jwt.InvalidSignatureError:
            raise HTTPException(status_code=401, detail="INVALID_TOKEN")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="EXPIRED_TOKEN")
        
        if not self.repository.get_account_by_email() is None:
            raise HTTPException(status_code=401, detail="ALREADY_REGISTERED_EMAIL")

        if USER_NAME_FORMAT.fullmatch(request.userName) is None:
            raise HTTPException(status_code=401, detail="INVALID_USER_NAME")
        
        if PASSWORD_FORMAT.fullmatch(request.password) is None:
            raise HTTPException(status_code=401, detail="INVALID_PASSWORD")
          
        account = self.repository.create_account(request.userName, userEmail, request.password)

        login_token = create_token(
            payload={
                "userId": encode_id(account.userId),
                "userName": account.userName
            },
            expire=86400 # 하루
        )
        
        response = Response()
        response.set_cookie(
            key="login_token",
            value=login_token,
            max_age=86400, # 하루
            httponly=True,
            samesite="strict",
            secure = not COOKIE_SECURE_OPTION is None
        )

        return response
