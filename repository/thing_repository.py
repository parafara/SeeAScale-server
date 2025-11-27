from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from model.thing_model import ThingCreateRequest
from utils.database import get_db
from utils.schema import Thing
from datetime import datetime
from typing import List

class ThingRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_thing(self, request: ThingCreateRequest, userId: int) -> Thing:
        now = datetime.now()
        thing = Thing(
            thingName = request.thingName,
            prefix = request.prefix,
            quantity = request.quantity,
            likesCount = 0,
            commentCount = 0,
            explanation = request.explaination,
            createdAt = now,
            modifiedAt = now,
            createdBy = userId
        )

        self.db.add(thing)
        self.db.commit()
        self.db.refresh(thing)

        return thing

    def get_thing_list(self, prefix: int, page: int) -> List[Thing]:
        statement = select(Thing).where(Thing.prefix == prefix).order_by(Thing.quantity).offset(page * 20).limit(20)
        return self.db.execute(statement).scalars().all()
    
    def get_thing(self, thingId: int) -> Thing | None:
        statement = select(Thing).where(Thing.thingId == thingId)
        return self.db.execute(statement).scalar_one_or_none()

    def modify_thing(
        self,
        thingId: int,
        thingName: str | None = None,
        prefix: int | None = None,
        quantity: int | None = None,
        explanation: str | None = None
    ) -> Thing | None:
        thing = self.get_thing(thingId=thingId)

        if thing is None:
            return thing
        
        if thingName:
            thing.thingName = thingName
        
        if quantity:
            thing.quantity = quantity

        if prefix:
            thing.prefix = prefix

        if explanation:
            thing.explanation = explanation

        thing.modifiedAt = datetime.now()

        self.db.commit()
        
        return thing

    def delete_thing(self, thingId: int) -> None:
        statement = select(Thing).where(Thing.thingId == thingId)
        thing = self.db.execute(statement).scalar_one_or_none()
        
        if thing:
            self.db.delete(thing)
        
        self.db.commit()