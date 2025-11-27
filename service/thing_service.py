from fastapi import Response, HTTPException, Depends
from repository.thing_repository import ThingRepository
from model.thing_model import ThingCreateRequest, ThingModifyRequest, ThingSummaryResponse, ThingResponse
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
    
    def get_thing_list(self, prefix: int, page: int):
        things = self.repository.get_thing_list(prefix, page)
        response = [
            ThingSummaryResponse(
                thingId = encode_id(i.thingId),
                thingName = i.thingName,
                prefix = i.prefix,
                quantity = str(i.quantity),
                likesCount = i.likesCount,
                commentCount = i.commentCount,
                createdAt = i.createdAt,
                modifiedAt = i.modifiedAt,
                createrId = encode_id(i.account.userId),
                createrName = i.account.userName
            ) for i in things
        ]

        return response

    def get_thing(self, thingId: str):
        thing = self.repository.get_thing(decode_id(thingId))

        response = Response(status_code=404)
        if thing:
            response = ThingResponse(
                thingId = encode_id(thing.thingId),
                thingName = thing.thingName,
                prefix = thing.prefix,
                quantity = str(thing.quantity),
                explanation = thing.explanation,
                likesCount = thing.likesCount,
                commentCount = thing.commentCount,
                createdAt = thing.createdAt,
                modifiedAt = thing.modifiedAt,
                createrId = encode_id(thing.account.userId),
                createrName = thing.account.userName
            )
        
        return response

    def modify_thing(self, request: ThingModifyRequest, thingId: str, login_token: dict):
        thingId: int = decode_id(thingId)
        userId = decode_id(login_token["userId"])
        
        thing = self.repository.get_thing(thingId=thingId)

        if thing is None:
            return HTTPException(status_code=404)
        
        if thing.account.userId != userId:
            raise HTTPException(status_code=403)
        
        thing = self.repository.modify_thing(
            thingId = thingId,
            thingName = request.thingName,
            prefix = request.prefix,
            quantity = request.quantity,
            explanation = request.explaination
        )

        response = ThingResponse(
            thingId = encode_id(thing.thingId),
            thingName = thing.thingName,
            prefix = thing.prefix,
            quantity = str(thing.quantity),
            explanation = thing.explanation,
            likesCount = thing.likesCount,
            commentCount = thing.commentCount,
            createdAt = thing.createdAt,
            modifiedAt = thing.modifiedAt,
            createrId = encode_id(thing.account.userId),
            createrName = thing.account.userName
        )
        
        return response

    def delete_thing(self, thingId: str, login_token: dict):
        thingId: int = decode_id(thingId)
        userId: int = decode_id(login_token["userId"])

        thing = self.repository.get_thing(thingId=thingId)
        
        if thing.account.userId != userId:
            raise HTTPException(status_code=403)
        
        self.repository.delete_thing(thingId)

        return Response(status_code=200)
