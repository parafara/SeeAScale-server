from fastapi import Depends
from repository.ThingRepository import ThingRepsitory, Thing
from dto.ThingDto import ThingSummaryInternalDto, ThingInternalDto
from utils.constant import IMAGE_STORAGE_PATH
from decimal import Decimal, ROUND_DOWN
from PIL import Image
from io import BytesIO
import os

class ThingServiceException:
    class WrongImageFormat(Exception): pass
    class NotFoundThing(Exception): pass
    class OutOfQuantityRange(Exception): pass
    class NoAuthoiry(Exception): pass

class ThingService:
    def __init__(self, repository: ThingRepsitory = Depends()):
        self.repository = repository

    def create(
            self,
            title: str, imageData: bytes, prefix: int, quantity: Decimal, explanation: str,
            createrId: int
        ) -> ThingInternalDto:
        prefix, quantity = unit_standardization(prefix, quantity)
        imageFile = BytesIO(imageData)
        if quantity.adjusted() > 2: raise ThingServiceException.OutOfQuantityRange()
        try: image = Image.open(imageFile).convert(mode="RGB")
        except: raise ThingServiceException.WrongImageFormat()
        processedImage = process_image(image)
        thing = self.repository.create(title, prefix, quantity, explanation, createrId)
        processedImage.save(f"{IMAGE_STORAGE_PATH}/{thing.thingId}.jpeg", format="JPEG")
        processedImage.close()
        
        result = thing2summary(thing)
        result = ThingInternalDto(**result.model_dump(), explanation=thing.explanation, mine=True, liked=False)
        
        self.repository.commit()
        return result

    def get_list(self, prefix: int, page: int, byAsc: bool) -> list[ThingSummaryInternalDto]:
        things = self.repository.get_list(prefix, page, byAsc)
        result = [thing2summary(thing) for thing in things]
        return result
    
    def get(self, thingId: int, accountId: int | None) -> ThingInternalDto:
        thing = self.repository.get(thingId)
        if accountId: liked = self.repository.is_liked(thingId, accountId)
        else: liked = False
        if thing is None: raise ThingServiceException.NotFoundThing()
        result = thing2summary(thing)
        result = ThingInternalDto(
            **result.model_dump(),
            explanation = thing.explanation, 
            mine = thing.createrId == accountId, liked = liked
        )
        return result

    def update(
        self,
        thingId: int, accountId: int,
        title: str | None = None, imageFile: BytesIO | None = None, 
        prefix: int | None = None, quantity: Decimal | None = None, 
        explanation: str | None = None
    ) -> ThingInternalDto:
        thing = self.repository.get(thingId)
        if thing is None: raise ThingServiceException.NotFoundThing()
        if thing.createrId != accountId: raise ThingServiceException.NoAuthoiry()
        if imageFile:
            try: image = Image.open(imageFile).convert(mode="RGB")
            except: raise ThingServiceException.WrongImageFormat()
            processedImage = process_image(image)
            processedImage.save(f"{IMAGE_STORAGE_PATH}/{thing.thingId}.jpeg", format="JPEG")
            processedImage.close()
        thing = self.repository.update(thingId, title, prefix, quantity, explanation)
        liked = self.repository.is_liked(thingId, accountId)
        result = thing2summary(thing)
        result = ThingInternalDto(**result.model_dump(), explanation=thing.explanation, mine=True, liked=liked)
        self.repository.commit()
        return result
    
    def delete(self, thingId: int, accountId: int) -> None:
        thing = self.repository.get(thingId)
        if thing is None: raise ThingServiceException.NotFoundThing()
        if thing.createrId != accountId: raise ThingServiceException.NoAuthoiry()
        try: os.remove(f"{IMAGE_STORAGE_PATH}/{thing.thingId}.jpeg")
        except: pass
        self.repository.delete(thingId)
        self.repository.commit()

def thing2summary(thing: Thing) -> ThingSummaryInternalDto:
    result = ThingSummaryInternalDto.model_validate(thing)
    result.createrName = thing.creater.name
    return result

def process_image(image: Image.Image) -> Image.Image:
    w, h = image.size
    max_side = max(w, h)
    processedImage = Image.new("RGB", (max_side, max_side), (255, 255, 255))
    offset = ((max_side - w) // 2, (max_side - h) // 2)
    processedImage.paste(image, offset)
    processedImage = processedImage.resize((1024, 1024), Image.Resampling.LANCZOS)
    return processedImage

def unit_standardization(prefix: int, quantity: Decimal) -> Decimal:
    while prefix > 3 and quantity < 1:
        prefix -= 1
        quantity *= 1000
    while 3 >= prefix > -3 and quantity < 1:
        prefix -= 1
        quantity *= 10
    while -3 >= prefix > -10 and quantity < 1:
        prefix -= 1
        quantity *= 1000
    while prefix < -3 and quantity >= 1000:
        prefix += 1
        quantity /= 1000
    while -3 <= prefix < 3 and quantity >= 10:
        prefix += 1
        quantity /= 10
    while 3 <= prefix < 10 and quantity >= 1000:
        prefix += 1
        quantity /= 1000
    quantity = quantity.quantize(Decimal("0.00"), rounding=ROUND_DOWN)
    return prefix, quantity
