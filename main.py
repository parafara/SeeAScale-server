from fastapi import FastAPI
from utils.middleware import exception_catcher
from router import AccountRouter, ThingRouter, CommentRouter, LikeRouter

app = FastAPI()

app.middleware("http")(exception_catcher)

app.include_router(AccountRouter.router)
app.include_router(ThingRouter.router)
app.include_router(CommentRouter.router)
app.include_router(LikeRouter.router)