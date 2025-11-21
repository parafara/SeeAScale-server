from fastapi import Depends
from schema import Account
from sqlalchemy.orm import Session
from database import get_db
from utils.crypto_tools import hash_password

class AccountRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db=db

    def get_account_by_userEmail(self, userEmail: str) -> Account | None:
        return self.db.query(Account).filter_by(userEmail=userEmail).first()
    
    def create_account(self, userName, userEmail, password) -> Account:
        account = Account(userName=userName, userEmail=userEmail, passwordHash=hash_password(password))

        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        
        return account