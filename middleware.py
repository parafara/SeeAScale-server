from fastapi import Request
from fastapi.responses import JSONResponse
from model.exceptions import LoginTokenExpiredException

async def exception_catcher(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except LoginTokenExpiredException:
        response = JSONResponse({"code":"EXPIRED_TOKEN"}, status_code=401)
        response.delete_cookie(key="login_token", httponly=True, samesite="strict")
        return response