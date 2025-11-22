from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.constant import DB_URL, RELEASE

engine = create_engine(DB_URL, echo=not RELEASE, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
