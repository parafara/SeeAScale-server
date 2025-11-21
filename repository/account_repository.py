from fastapi import Depends
from schema import Account
from sqlalchemy.orm import Session
from database import get_db

class AccountRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db=db

    def get_account_by_email(self, email: str) -> Account | None:
        return self.db.query(Account).filter_by(userEmail=email).first()