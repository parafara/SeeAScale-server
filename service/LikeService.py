from fastapi import Depends
from repository.LikeRepository import LikeRepository

class LikeService:
    def __init__(self, repository: LikeRepository = Depends()):
        self.repository = repository

    def create(self, thingId: int, accountId: int):
        self.repository.create(thingId, accountId)
        self.repository.commit()

    def delete(self, thingId: int, accountId: int):
        self.repository.delete(thingId, accountId)
        self.repository.commit()
    