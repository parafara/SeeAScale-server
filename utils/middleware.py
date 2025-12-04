from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from utils.crypto_manager import CryptoManagerException
from utils.constant import INVALID_TOKEN, EXPIRED_TOKEN

async def exception_catcher(request: Request, next_call):
    try:
        try:
            response = await next_call(request)
            return response
        except CryptoManagerException.InvalidToken:
            raise HTTPException(status_code=401, detail=INVALID_TOKEN)
        except CryptoManagerException.ExpiredToken:
            raise HTTPException(status_code=401, detail=EXPIRED_TOKEN)
        except CryptoManagerException.InvalidId:
            raise HTTPException(status_code=404)
    except HTTPException as e:
        response = JSONResponse(
            {"detail": e.detail},
            status_code = e.status_code,
            headers = e.headers
        )
        return response