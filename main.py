from fastapi import FastAPI
from utils.middleware import exception_catcher

app = FastAPI()

app.middleware("http")(exception_catcher)
