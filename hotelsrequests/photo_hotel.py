from random import sample

from .connector import get_requests
from config import SERCH_PHOTO_HOTEL_URL

async def get_photo_urls(id_hotel: int, count_photo: int) -> list[str]:
    params = {'id': id_hotel}
    result = await get_requests(SERCH_PHOTO_HOTEL_URL, params)

    if not result:
        return None

    result = result['hotelImages']
    if len(result) > count_photo:
        result = sample(result, count_photo)

    result = [image['baseUrl'].format(size='z') for image in result]
    return result
