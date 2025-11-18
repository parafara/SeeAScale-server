from fastapi import APIRouter, Response, Depends
from fastapi.responses import JSONResponse
from database import get_db
from model.dto import PreRegisterDTO
from service.auth import verify_email_format, check_email_register_status, send_auth_mail

router = APIRouter(prefix="/auth", tags=["/auth"])

@router.post("/preregister")
def post_preregister(data: PreRegisterDTO, db=Depends(get_db)):
    if not verify_email_format(data.email):
        return JSONResponse({"code": "INVALID_EMAIL_FORMAT"}, status_code=400)
    
    if check_email_register_status(data.email, db):
        return JSONResponse({"code": "ALREADY_REGISTERED"}, status_code=400)
    
    send_auth_mail(data.email)

    return Response()