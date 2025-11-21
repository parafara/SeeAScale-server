from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, BINARY

class Base(DeclarativeBase):
    pass

class Account(Base):
    __tablename__ = "account"

    userId: Mapped[int] = mapped_column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    userName: Mapped[str] = mapped_column(VARCHAR(16), nullable=False)
    userEmail: Mapped[str] = mapped_column(VARCHAR(100), index=True, unique=True, nullable=False)
    passwordHash: Mapped[bytes] = mapped_column(BINARY(32), nullable=False)

if __name__ == "__main__":
    from database import engine

    Base.metadata.create_all(bind=engine)