from bs4 import BeautifulSoup

from .connector import get_requests


async def search_locations(params: dict) -> dict:

    SERCH_LOCATION_URL = f'https://hotels4.p.rapidapi.com/locations/v2/search'

    result = await get_requests(SERCH_LOCATION_URL, params)
    
    if not result:
        return None

    citys = filter(lambda dict_city: dict_city['type'] == 'CITY',
                   result['suggestions'][0]['entities'])

    return {city['destinationId']: BeautifulSoup(city['caption'], 'html.parser').text
            for city in citys}
    
