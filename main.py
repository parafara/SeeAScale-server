from fastapi import FastAPI
from database import engine, Base
import model.tables
from router import auth
from middleware import exception_catcher

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.middleware("http")(exception_catcher)

app.include_router(auth.router)
