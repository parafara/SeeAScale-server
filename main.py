from fastapi import FastAPI
from router import account_router, thing_router

app = FastAPI()

app.include_router(account_router.router)
app.include_router(thing_router.router)
