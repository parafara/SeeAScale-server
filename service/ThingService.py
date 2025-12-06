from fastapi import UploadFile, Depends
from repository.ThingRepository import ThingRepsitory
from dto.ThingDto import ThingInternalDto
from utils.constant import IMAGE_STORAGE_PATH
from decimal import Decimal, ROUND_DOWN
from PIL import Image
from io import BytesIO

class ThingServiceException:
    class WrongImageFormat(Exception): pass

class ThingService:
    def __init__(self, repository: ThingRepsitory = Depends()):
        self.repository = repository

    def create(self, title: str, imageFile: BytesIO, prefix: int, quantity: Decimal, explanation: str, createrId: int) -> ThingInternalDto:
        try:
            image = Image.open(imageFile).convert(mode="RGB")
        except Exception as e:
            raise ThingServiceException.WrongImageFormat()
        
        prefix, quantity = unit_standardization(prefix, quantity)

        w, h = image.size
        max_side = max(w, h)
        
        processedImage = Image.new("RGB", (max_side, max_side), (255, 255, 255))
        offset = ((max_side - w) // 2, (max_side - h) // 2)
        processedImage.paste(image, offset)
        processedImage = processedImage.resize((512, 512), Image.Resampling.LANCZOS)
        image.close()

        thing = self.repository.create(title, prefix, quantity, explanation, createrId)
        processedImage.save(f"{IMAGE_STORAGE_PATH}/{thing.thingId}.jpeg", format="JPEG")
        processedImage.close()

        result = ThingInternalDto.model_validate(thing)
        result.createrName = thing.creater.name

        self.repository.commit()
        return result

    def get(self, thingId: int) -> ThingInternalDto | None:
        thing = self.repository.get(thingId)

        if thing is None: return None

        result = ThingInternalDto.model_validate(thing)
        result.createrName = thing.creater.name

        return result

def unit_standardization(prefix: int, quantity: Decimal) -> Decimal:
    while prefix > 3 and quantity < 1:
        prefix -= 1
        quantity *= 1000

        print(prefix, quantity)
        
    while 3 >= prefix > -3 and quantity < 1:
        prefix -= 1
        quantity *= 10

        print(prefix, quantity)

    while -3 >= prefix > -10 and quantity < 1:
        prefix -= 1
        quantity *= 1000

        print(prefix, quantity)

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
