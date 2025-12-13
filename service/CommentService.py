from fastapi import Depends
from repository.CommentRepository import CommentRepository, Comment
from dto.CommentDto import CommentInternalDto

class CommentServiceException:
    class NotFoundThing(Exception): pass
    class NotFoundComment(Exception): pass
    class NoAuthority(Exception): pass

class CommentService:
    def __init__(self, repository: CommentRepository = Depends()):
        self.repository = repository
    
    def create(self, content: str, thingId: int, createrId: int) -> CommentInternalDto:
        thing = self.repository.get_thing(thingId)
        if thing is None: raise CommentServiceException.NotFoundThing()
        comment = self.repository.create(content, thingId, createrId)
        result = comment_to_internal_dto(comment)
        self.repository.commit()
        return result

    def get_list(self, thingId: int) -> list[CommentInternalDto]:
        comments = self.repository.get_list(thingId)
        if comments is None: raise CommentServiceException.NotFoundThing()

        result = [comment_to_internal_dto(comment) for comment in comments]

        return result
    
    def update(self, commentId: int, accountId: int, content: str) -> CommentInternalDto:
        comment = self.repository.get(commentId)
        if comment is None: raise CommentServiceException.NotFoundComment()
        if comment.createrId != accountId: raise CommentServiceException.NoAuthority()

        comment = self.repository.update(comment, content)

        result = comment_to_internal_dto(comment)
        self.repository.commit()
        return result
    
    def delete(self, commentId: int, accountId: int) -> None:

        comment = self.repository.get(commentId)
        if comment is None: raise CommentServiceException.NotFoundComment()
        if comment.createrId != accountId: raise CommentServiceException.NoAuthority()

        self.repository.delete(comment)
        self.repository.commit()

def comment_to_internal_dto(comment: Comment) -> CommentInternalDto:
    result = CommentInternalDto.model_validate(comment)
    result.createrName = comment.creater.name
    return result
