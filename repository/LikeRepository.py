from fastapi import Depends
from sqlalchemy import select, and_
from utils.database import Session, get_db
from utils.entity import Like

class LikeRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        
    def create(self, thingId: int, accountId: int) -> None:
        like = Like(thingId=thingId, accountId=accountId)
        self.db.add(like)
        return like
    
    def delete(self, thingId: int, accountId: int) -> None:
        statement = select(Like).where(and_(Like.thingId == thingId, Like.accountId == accountId))
        like = self.db.execute(statement).scalar_one_or_none()
        self.db.delete(like)

    def exist(self, thingId: int, accountId: int) -> bool:
        statement = select(Like).where(and_(Like.thingId == thingId, Like.accountId == accountId))
        like = self.db.execute(statement).scalar_one_or_none()
        return not like is None
    
    def commit(self):
        self.db.commit()