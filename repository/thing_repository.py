from fastapi import Depends
from sqlalchemy.orm import Session
from model.thing_model import ThingCreateRequest
from utils.database import get_db
from utils.schema import Thing
from datetime import datetime

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
