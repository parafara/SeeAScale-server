from fastapi import Depends
from repository.LikeRepository import LikeRepository

class LikeServiceException:
    class AlreadyLiked(Exception): pass
    class NotLiked(Exception): pass

class LikeService:
    def __init__(self, repository: LikeRepository = Depends()):
        self.repository = repository

    def create(self, thingId: int, accountId: int):
        if self.repository.exist(thingId, accountId): raise LikeServiceException.AlreadyLiked()
        self.repository.create(thingId, accountId)
        self.repository.commit()

    def delete(self, thingId: int, accountId: int):
        if not self.repository.exist(thingId, accountId): raise LikeServiceException.NotLiked()
        self.repository.delete(thingId, accountId)
        self.repository.commit()
    