import datetime
import aiohttp
from bs4 import BeautifulSoup
from config import HEADERS_REQUESTS, HOTELS_URL
from loguru import logger


async def search_locations(params: dict) -> dict:

    SERCH_LOCATION_URL = f'https://{HOTELS_URL}/locations/v2/search'

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=SERCH_LOCATION_URL,
                                   params=params,
                                   headers=HEADERS_REQUESTS
                                   ) as respons:
                result = await respons.json()

        except aiohttp.ClientError as error:
            logger.error(f"[{error.__class__.__name__}] {error}")
            return None

    citys = filter(lambda dict_city: dict_city['type'] == 'CITY',
                   result['suggestions'][0]['entities'])

    return {city['destinationId']: BeautifulSoup(city['caption'], 'html.parser').text
            for city in citys}


async def get_hotels(user_request: dict):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    params = {
        'destinationId': user_request['city_id'],
        'pageNumber': '1',
        'pageSize': user_request['count_hotel'],
        'checkIn': today.strftime('%Y-%m-%d'),
        'checkOut': tomorrow.strftime('%Y-%m-%d'),
        'adults1': '1',
        'locale': user_request['locale'],
        'currency': user_request['currency']
    }

    match user_request['request']:
        case '/highprice':
            params['sortOrder'] = 'PRICE_HIGHEST_FIRST'
        case '/lowprice':
            params['sortOrder'] = 'PRICE'
        case '/bestdeal':
            params['sortOrder'] = 'DISTANCE_FROM_LANDMARK'
            params['priceMin'] = user_request['begin_price']
            params['priceMax'] = user_request['end_price']
        case _:
            params['sortOrder'] = 'PRICE'

    result = await search_hotel(params)

    if user_request['request'] == '/bestdeal':
        return await filter_bestdeal(result, user_request['radius'])
    return result


async def search_hotel(params: dict):

    SERCH_LOCATION_URL = 'https://hotels4.p.rapidapi.com/properties/list'

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=SERCH_LOCATION_URL,
                                   params=params,
                                   headers=HEADERS_REQUESTS
                                   ) as respons:
                respons_hotels = await respons.json()

        except aiohttp.ClientError as error:
            print(f"{error.__class__.__name__}  {error}")
            return None

    results = respons_hotels['data']['body']['searchResults']['results']

    hotels = [{
        'name': hotel['name'],
        'addres': hotel['address']['streetAddress'],
        'rating': hotel['starRating'],
        'price': hotel['ratePlan']['price']['current'],
        'location': ', '.join([f"{place['label']} - {place['distance']}" for place in hotel['landmarks']])
    } for hotel in results]

    return hotels


async def filter_bestdeal(hotels, radius):
    return hotels
