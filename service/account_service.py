from fastapi import Response, HTTPException, Depends
from repository.account_repository import AccountRepository
from utils.tokener import create_token
from utils.mail import send_preregister_mail
import re

EMAIL_FORMAT = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

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