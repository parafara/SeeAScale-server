from fastapi import Depends
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.schema import Account
from utils.crypto_manager import hash_password

class AccountRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db=db

    def create_account(self, userName, userEmail, password) -> Account:
        account = Account(userName=userName, userEmail=userEmail, passwordHash=hash_password(password))

        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        
        return account

    def get_account_by_userEmail(self, userEmail: str) -> Account | None:
        return self.db.query(Account).filter_by(userEmail=userEmail).first()
