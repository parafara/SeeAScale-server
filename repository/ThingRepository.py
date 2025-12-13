from fastapi import Depends
from sqlalchemy import select, and_, asc, desc
from utils.database import Session, get_db
from utils.entity import Thing, Like
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
    
    def get_list(self, prefix: int, page: int, byAsc: bool) -> list[Thing]:
        orderBy = asc(Thing.quantity) if byAsc else desc(Thing.quantity)
        statement = select(Thing).where(Thing.prefix == prefix).order_by(orderBy).offset(page * 20).limit(20)
        return self.db.execute(statement).scalars().all()

    def get(self, thingId: int) -> Thing | None:
        statement = select(Thing).where(Thing.thingId == thingId)
        return self.db.execute(statement).scalar_one_or_none()
    
    def update(
        self,
        thingId: int,
        title: str | None = None, prefix: int | None = None,
        quantity: Decimal | None = None, explanation: str | None = None
    ) -> Thing:
        thing = self.get(thingId)
        if title: thing.title = title
        if prefix: thing.prefix = prefix
        if quantity: thing.quantity = quantity
        if explanation: thing.explanation = explanation
        thing.modifiedAt = datetime.now()
        return thing

    def delete(self, thingId: int) -> None:
        thing = self.get(thingId)
        self.db.delete(thing)

    def is_liked(self, thingId: int, accountId: int) -> bool:
        statement = select(Like).where(and_(Like.thingId == thingId, Like.accountId == accountId))
        like = self.db.execute(statement).scalar_one_or_none()
        return not like is None

    def commit(self):
        self.db.commit()