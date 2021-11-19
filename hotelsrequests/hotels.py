import datetime
from .connector import get_requests


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

    result = await get_requests(SERCH_LOCATION_URL, params)

    if not result:
        return None
    
    result = result['data']['body']['searchResults']['results']

    hotels = [{
        'name': hotel['name'],
        'addres': hotel['address']['streetAddress'],
        'rating': hotel['starRating'],
        'price': hotel['ratePlan']['price']['current'],
        'location': hotel['landmarks']
    } for hotel in result]

    return hotels

async def filter_bestdeal(hotels, radius):
    return hotels