from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import INTEGER, DECIMAL, VARCHAR, BINARY, TINYINT, DATETIME
from datetime import datetime
from decimal import Decimal
from typing import List

class Base(DeclarativeBase):
    pass

class Account(Base):
    __tablename__ = "Account"

    accountId: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(VARCHAR(100), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(VARCHAR(32), nullable=False)
    hashedPassword: Mapped[bytes] = mapped_column(BINARY(32), nullable=False)

    things: Mapped[List["Thing"]] = relationship("Thing", back_populates="creater")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="creater")
    likes: Mapped[List["Like"]] = relationship("Like", back_populates="account")

class Thing(Base):
    __tablename__ = "Thing"

    thingId: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(VARCHAR(32), nullable=False)
    prefix: Mapped[int] = mapped_column(TINYINT, nullable=False)
    quantity: Mapped[Decimal] = mapped_column(DECIMAL(5, 2, unsigned=True), nullable=False)
    explanation: Mapped[str] = mapped_column(VARCHAR(500), nullable=False)
    likesCount: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False)
    commentCount: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
    modifiedAt: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
    createrId: Mapped[int] = mapped_column(INTEGER(unsigned=True), ForeignKey("Account.accountId"), nullable=False)

    creater: Mapped["Account"] = relationship("Account", back_populates="things")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="thing", cascade="all, delete-orphan")
    likes: Mapped[List["Like"]] = relationship("Like", back_populates="thing", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("prefix >= -10 AND prefix <= 10", name="check_prefix_range"),
    )

class Comment(Base):
    __tablename__ = "Comment"

    commentId: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
    modifiedAt: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
    createrId: Mapped[int] = mapped_column(INTEGER(unsigned=True), ForeignKey("Account.accountId"), nullable=False)
    thingId: Mapped[int] = mapped_column(INTEGER(unsigned=True), ForeignKey("Thing.thingId", ondelete="CASCADE"), nullable=False)
    
    creater: Mapped["Account"] = relationship("Account", back_populates="comments")
    thing: Mapped["Thing"] = relationship("Thing", back_populates="comments")

class Like(Base):
    __tablename__ = "Like"

    accountId: Mapped[int] = mapped_column(INTEGER(unsigned=True), ForeignKey("Account.accountId"), primary_key=True)
    thingId: Mapped[int] = mapped_column(INTEGER(unsigned=True), ForeignKey("Thing.thingId", ondelete="CASCADE"), primary_key=True)

    account: Mapped["Account"] = relationship("Account", back_populates="likes")
    thing: Mapped["Thing"] = relationship("Thing", back_populates="likes")

if __name__ == "__main__":
    from database import engine

    # Base.metadata.drop_all(bind=engine) # 테이블 DROP
    Base.metadata.create_all(bind=engine) # 테이블 CREATE
