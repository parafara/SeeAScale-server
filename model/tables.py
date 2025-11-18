from sqlalchemy import Column, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, VARCHAR, BINARY, TEXT, DATETIME
from database import Base

class Account(Base):
    __tablename__ = "account"

    user_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    user_name = Column(VARCHAR(16), nullable=False)
    email = Column(VARCHAR(100), nullable=False, unique=True)
    password_hash = Column(BINARY(32), nullable=False)

    # relationship
    objects_created = relationship("Object", back_populates="creator")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")


class Object(Base):
    __tablename__ = "object"

    object_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    object_name = Column(VARCHAR(32), nullable=False)
    image_url = Column(VARCHAR(128), nullable=False)
    prefix = Column(TINYINT, CheckConstraint('prefix >= -10 AND prefix <= 10'), nullable=False)
    quantity = Column(TINYINT(unsigned=True), nullable=False)
    likes_count = Column(INTEGER(unsigned=True), nullable=False)
    comment_count = Column(INTEGER(unsigned=True), nullable=False)
    explaination = Column(TEXT, nullable=False)
    created_at = Column(DATETIME, nullable=False)
    created_by = Column(INTEGER(unsigned=True), ForeignKey("account.user_id"), nullable=False)

    # relationship
    creator = relationship("Account", back_populates="objects_created")
    comments = relationship("Comment", back_populates="object")
    liked_by = relationship("Like", back_populates="object")


class Comment(Base):
    __tablename__ = "comment"

    comment_id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column(INTEGER(unsigned=True), ForeignKey("account.user_id"), nullable=False)
    object_id = Column(INTEGER(unsigned=True), ForeignKey("object.object_id"), nullable=False)
    content = Column(TEXT, nullable=False)

    # relationship
    user = relationship("Account", back_populates="comments")
    object = relationship("Object", back_populates="comments")


class Like(Base):
    __tablename__ = "likes"

    user_id = Column(INTEGER(unsigned=True), ForeignKey("account.user_id"), primary_key=True)
    object_id = Column(INTEGER(unsigned=True), ForeignKey("object.object_id"), primary_key=True)

    # relationship
    user = relationship("Account", back_populates="likes")
    object = relationship("Object", back_populates="liked_by")
