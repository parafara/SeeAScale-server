from fastapi import Depends
from sqlalchemy import select
from utils.database import Session, get_db
from utils.entity import Account

class AccountRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, email: str, name: str, hashedPassword: bytes) -> Account:
        account = Account(email=email, name=name, hashedPassword=hashedPassword)
        self.db.add(account)
        self.db.flush()
        self.db.refresh(account)
        return account
    
    def get_by_email(self, email: str) -> Account | None:
        statement = select(Account).where(Account.email == email)
        account = self.db.execute(statement).scalar_one_or_none()
        return account

    def commit(self) -> None:
        self.db.commit()