from fastapi import APIRouter

router = APIRouter(prefix='', tags=['root'])

@router.get("/")
def get_root():
    return {"message": "hello world"}