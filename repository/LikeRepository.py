from fastapi import Depends
from sqlalchemy import select, and_
from utils.database import Session, get_db
from utils.entity import Like

class LikeRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        
    def create(self, thingId: int, accountId: int):
        like = Like(thingId=thingId, createrId=accountId)
        self.db.add(like)
        return like
    
    def delete(self, thingId: int, accountId: int):
        statement = select(Like).where(and_(Like.thingId == thingId, Like.creater == accountId))
        like = self.db.execute(statement)
        self.db.delete(like)
    
    def commit(self):
        self.db.commit()