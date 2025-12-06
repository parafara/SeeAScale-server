from fastapi import Depends
from sqlalchemy import select
from utils.database import Session, get_db
from utils.entity import Thing
from datetime import datetime
from decimal import Decimal

class ThingRepsitory:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
    
    def create(self, title: str, prefix: int, quantity: Decimal, explanation: str, createrId: int) -> Thing:
        now = datetime.now()

        thing = Thing(
            title=title,
            prefix=prefix,
            quantity=quantity,
            explanation=explanation,
            likesCount=0,
            commentCount=0,
            createdAt=now,
            modifiedAt=now,
            createrId=createrId
        )
        
        self.db.add(thing)
        self.db.flush()
        self.db.refresh(thing)

        return thing
    
    def get(self, thingId: int) -> Thing | None:
        statement = select(Thing).where(Thing.thingId == thingId)
        return self.db.execute(statement).scalar_one_or_none()
    
    def get_list(self, prefix: int, page: int) -> list[Thing]:
        statement = select(Thing).where(Thing.prefix == prefix).order_by(Thing.quantity).offset(page * 20).limit(20)
        return self.db.execute(statement).scalars().all()
    
    def commit(self):
        self.db.commit()