from fastapi import HTTPException, Depends
from repository.thing_repository import ThingRepository
from model.thing_model import ThingCreateRequest, ThingSummaryResponse
from utils.crypto_manager import encode_id, decode_id
from utils.mecro import unit_standardization
from utils.constant import IMAGE_STORAGE_PATH
from PIL import Image
from io import BytesIO

class ThingSerivce:
    def __init__(self, repository: ThingRepository = Depends()):
        self.repository = repository

    def create_thing(self, request: ThingCreateRequest, imageFile: bytes, login_token: dict):
        try:
            thingImage = Image.open(BytesIO(imageFile))
            thingImage.verify()
            thingImage = thingImage.convert("RGB")
        except Exception:
            raise HTTPException(status_code=422, detail="WRONG_IMAGE_FORMAT")

        request.quantity, request.prefix = unit_standardization(request.quantity, request.prefix)

        userId = decode_id(login_token["userId"])
        thing = self.repository.create_thing(request, userId)

        w, h = thingImage.size
        max_side = max(w, h)
        
        canvas = Image.new("RGB", (max_side, max_side), (255, 255, 255))
        offset = ((max_side - w) // 2, (max_side - h) // 2)
        canvas.paste(thingImage, offset)
        canvas = canvas.resize((512, 512), Image.LANCZOS)
        
        canvas.save(f"{IMAGE_STORAGE_PATH}/{thing.thingId}.jpg", format="JPEG", quality=90)
        canvas.close()
        thingImage.close()

        response = ThingSummaryResponse(
            thingId = encode_id(thing.thingId),
            thingName = thing.thingName,
            prefix = thing.prefix,
            quantity = str(thing.quantity),
            likesCount = thing.likesCount,
            commentCount = thing.commentCount,
            createdAt = thing.createdAt,
            modifiedAt = thing.modifiedAt,
            createrId = encode_id(thing.account.userId),
            createrName = thing.account.userName
        )

        return response