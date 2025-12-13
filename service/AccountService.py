from fastapi import Depends
from repository.AccountRepository import AccountRepository
from dto.AccountDto import AccountInternalDto
from utils.crypto_manager import encrypt_dict, decrypt_dict, hash_password
from utils.mail_manager import send_preregister_mail
from utils.constant import SIGN_UP_TOKEN_EXPIRY_PERIOD
import time

class AccountServiceException:
    class AreadyRegisteredEmail(Exception): pass
    class InvalidSignupToken(Exception): pass
    class ExpiredSignupToken(Exception): pass
    class UnregisteredEmail(Exception): pass
    class IncorrectPassword(Exception): pass

class AccountService:
    def __init__(self, repository: AccountRepository = Depends()):
        self.repository = repository

    def preregister(self, email: str, name: str, password: str) -> None:
        if not self.repository.get_by_email(email) is None:
            raise AccountServiceException.AreadyRegisteredEmail()
        
        hashedPassword = hash_password(password)
        payload = {
            "email": email,
            "name": name,
            "hashedPassword": hashedPassword.hex(),
            "exp": int(time.time()) + SIGN_UP_TOKEN_EXPIRY_PERIOD
        }
        signUpToken = encrypt_dict(payload)
        
        send_preregister_mail(email, signUpToken)
    
    def create(self, signUpToken: str) -> AccountInternalDto:
        try:
            payload = decrypt_dict(signUpToken)
        except:
            raise AccountServiceException.InvalidSignupToken()
        if payload["exp"] < int(time.time()):
            raise AccountServiceException.ExpiredSignupToken()

        email = payload["email"]
        name = payload["name"]
        hashedPassword = bytes.fromhex(payload["hashedPassword"])
        if not self.repository.get_by_email(email) is None:
            raise AccountServiceException.AreadyRegisteredEmail()
        account = self.repository.create(email, name, hashedPassword)
        result = AccountInternalDto.model_validate(account)

        self.repository.commit()
        return result
    
    def login(self, email: str, password: str):
        account = self.repository.get_by_email(email)
        if account is None:
            raise AccountServiceException.UnregisteredEmail()
        if account.hashedPassword != hash_password(password):
            raise AccountServiceException.IncorrectPassword()
        result = AccountInternalDto.model_validate(account)
        
        return result
