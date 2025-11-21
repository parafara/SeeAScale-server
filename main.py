from fastapi import FastAPI
from router import account_router

app = FastAPI()

app.include_router(account_router.router)
