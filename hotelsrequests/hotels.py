import datetime

from loguru import logger

from config import SERCH_HOTEL_URL, HOTEL_URL_FORMAT
from .connector import get_requests


async def get_hotels(user_dialog: dict) -> list[dict]:
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    user_request = user_dialog['request']
    
    params = {
        'destinationId': user_dialog['city_id'],
        'pageNumber': 1,
        'pageSize': user_dialog['count_hotel'],
        'checkIn': today.strftime('%Y-%m-%d'),
        'checkOut': tomorrow.strftime('%Y-%m-%d'),
        'adults1': '1',
        'sortOrder': 'PRICE',
        'locale': user_dialog['locale'],
        'currency': user_dialog['currency']
    }

    if user_request == '/highprice':
        params['sortOrder'] = 'PRICE_HIGHEST_FIRST'

    elif user_request == '/bestdeal':
        params['sortOrder'] = 'DISTANCE_FROM_LANDMARK'
        params['priceMin'] = user_dialog['begin_price']
        params['priceMax'] = user_dialog['end_price']

    result = await search_hotel(params)

    if user_request == '/bestdeal':
        result = await filter_bestdeal(result, user_dialog['radius'])
    
    return result


@logger.catch
async def search_hotel(params: dict) -> list[dict]:
    result = await get_requests(SERCH_HOTEL_URL, params)
    
    if not result:
        return None
    
    result = result['data']['body']['searchResults']['results']
    
    return [{
        'id_hotel': hotel['id'],
        'url_hotel': HOTEL_URL_FORMAT.format(hotel_id=hotel['id']),
        'name': hotel['name'],
        'addres': hotel['address']['streetAddress'],
        'rating': hotel['starRating'],
        'price': hotel['ratePlan']['price']['current'],
        'location': hotel['landmarks']
    } for hotel in result]


@logger.catch
async def filter_bestdeal(hotels: list[dict], radius: int) -> list[dict]:
    result = []
    
    for hotel in hotels:
        hotel_dist:str = hotel['location'][0]['distance'].split()[0]
        
        if ',' in hotel_dist:
            hotel_dist = hotel_dist.replace(',', '.')
            
        if radius > float(hotel_dist):
            result.append(hotel)
            
    return result
