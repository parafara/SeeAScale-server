from fastapi import APIRouter, UploadFile, File, Depends
from service.thing_service import ThingSerivce
from model.thing_model import ThingCreateRequest, ThingModifyRequest
from utils.preprocessor import thing_create_form, get_login_token

router = APIRouter(prefix="/thing", tags=["thing"])

@router.post("")
async def create_thing(
    request: ThingCreateRequest = Depends(thing_create_form),
    imageFile: UploadFile = File(),
    login_token: dict = Depends(get_login_token),
    service: ThingSerivce = Depends()
):
    return service.create_thing(request=request, imageFile = await imageFile.read(), login_token=login_token)

@router.get("")
def get_thing_list(prefix: int = 0, page: int = 0, service: ThingSerivce = Depends()):
    return service.get_thing_list(prefix, page)

@router.get("/{thingId:str}")
def get_thing(thingId: str, service: ThingSerivce = Depends()):
    return service.get_thing(thingId)

@router.patch("/{thingId:str}")
def modify_thing(request: ThingModifyRequest, thingId: str, login_token: dict = Depends(get_login_token), service: ThingSerivce = Depends()):
    return service.modify_thing(request, thingId, login_token)

@router.delete("/{thingId:str}")
def delete_thing(thingId: str, login_token: dict = Depends(get_login_token), service: ThingSerivce = Depends()):
    return service.delete_thing(thingId, login_token)