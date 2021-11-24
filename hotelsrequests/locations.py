from bs4 import BeautifulSoup

from .connector import get_requests
from config import SERCH_LOCATION_URL

async def search_locations(params: dict) -> dict[int, str]:
    result = await get_requests(SERCH_LOCATION_URL, params)

    if not result:
        return None

    cities = filter(lambda dict_city: dict_city['type'] == 'CITY',
                   result['suggestions'][0]['entities'])

    return {city['destinationId']: BeautifulSoup(city['caption'], 'html.parser').text
            for city in cities}
