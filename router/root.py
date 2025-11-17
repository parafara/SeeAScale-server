from fastapi import APIRouter
from service.root import read_root_message

router = APIRouter(prefix='', tags=['root'])

@router.get("/")
def get_root():
    return read_root_message()