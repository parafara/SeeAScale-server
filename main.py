from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import AccountRouter, ThingRouter, CommentRouter, LikeRouter
from utils.exception_catcher import register_exception_handler
from utils.constant import FRONTEND_HOST

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:4173",
        FRONTEND_HOST
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

register_exception_handler(app)

app.include_router(AccountRouter.router)
app.include_router(ThingRouter.router)
app.include_router(CommentRouter.router)
app.include_router(LikeRouter.router)