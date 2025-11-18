from fastapi import FastAPI
from database import engine, Base
import model.tables
from router import auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
