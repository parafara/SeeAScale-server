from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, BINARY, TINYINT, DATETIME
from datetime import datetime
from typing import List

class Base(DeclarativeBase):
    pass

class Account(Base):
    __tablename__ = "Account"

    userId: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    userName: Mapped[str] = mapped_column(VARCHAR(16), nullable=False)
    userEmail: Mapped[str] = mapped_column(VARCHAR(100), index=True, unique=True, nullable=False)
    passwordHash: Mapped[bytes] = mapped_column(BINARY(32), nullable=False)

    things: Mapped[List["Thing"]] = relationship("Thing", back_populates="account")

class Thing(Base):
    __tablename__ = "Thing"

    thingId: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    thingName: Mapped[str] = mapped_column(VARCHAR(32), nullable=False)
    prefix: Mapped[int] = mapped_column(TINYINT, nullable=False)
    quantity: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False)
    likesCount: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False)
    commentCount: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False)
    explaination: Mapped[str] = mapped_column(VARCHAR(500), nullable=False)
    createdAt: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
    modifiedAt: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
    createdBy: Mapped[int] = mapped_column(INTEGER(unsigned=True), ForeignKey("Account.userId"), nullable=False)

    account: Mapped["Account"] = relationship("Account", back_populates="things")

    __table_args__ = (
        CheckConstraint("quantity >= -10 AND quantity <= 10", name="check_quantity_range"),
    )

if __name__ == "__main__":
    from database import engine

    # Base.metadata.drop_all(bind=engine) # 테이블 DROP
    Base.metadata.create_all(bind=engine) # 테이블 CREATE
