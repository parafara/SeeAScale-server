from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
try:
    from utils.constant import DB_URL, RELEASE
except ModuleNotFoundError:
    from constant import DB_URL, RELEASE

engine = create_engine(DB_URL, echo=not RELEASE, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
