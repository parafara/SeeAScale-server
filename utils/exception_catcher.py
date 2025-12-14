from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from utils.crypto_manager import CryptoManagerException
from utils.request_manager import RequestManagerException
from utils.constant import INVALID_TOKEN, EXPIRED_TOKEN, NOT_LOGGED_IN, INVALID_ID

def register_exception_handler(app: FastAPI):
    @app.exception_handler(CryptoManagerException.InvalidToken)
    async def InvalidToken_handler(request: Request, exc):
        return JSONResponse({"detail": INVALID_TOKEN}, status_code=401)

    @app.exception_handler(CryptoManagerException.ExpiredToken)
    async def ExpiredToken_handler(request: Request, exc):
        return JSONResponse({"detail": EXPIRED_TOKEN}, status_code=401)
    
    @app.exception_handler(RequestManagerException.NotLoggedIn)
    async def NotLoggedIn_handler(request: Request, exc):
        return JSONResponse({"detail": NOT_LOGGED_IN}, status_code=401)
    
    @app.exception_handler(CryptoManagerException.InvalidId)
    async def InvalidId_handler(request: Request, exc):
        return JSONResponse({"detail": INVALID_ID}, status_code=404)