from requests import get, exceptions
from bs4 import BeautifulSoup
from config import HEADERS_REQUESTS, HOTELS_URL
from loguru import logger


def search_locations(city_request: dict) -> dict:
    params = {
        'query': city_request['city'],
        'locale': city_request['locale'],
        'currency': city_request['currency']
    }
    try:
        result = get(
            url=f'https://{HOTELS_URL}/locations/v2/search',
            params=params,
            headers=HEADERS_REQUESTS
        )
        logger.info(
            f"[API HOTELS] Request to {HOTELS_URL} has status code {result.status_code}")
    except exceptions.RequestException as error:
        logger.error(
            f"[API HOTELS] Request to {HOTELS_URL} has exception {error}")
        return None
    
    citys = filter(lambda dict_city: dict_city['type'] == 'CITY',
                   result.json()['suggestions'][0]['entities'])

    return {city['destinationId']: BeautifulSoup(city['caption'], 'html.parser').text
            for city in citys}
