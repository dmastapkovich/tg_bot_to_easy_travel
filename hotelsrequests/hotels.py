import datetime
from .connector import get_requests


async def get_hotels(user_dialog: dict):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    user_request = user_dialog['request']
    params = {
        'destinationId': user_dialog['city_id'],
        'pageNumber': '1',
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
        return await filter_bestdeal(result, user_dialog['radius'])
    return result


async def search_hotel(params: dict):

    SERCH_LOCATION_URL = 'https://hotels4.p.rapidapi.com/properties/list'

    result = await get_requests(SERCH_LOCATION_URL, params)

    if not result:
        return None

    result = result['data']['body']['searchResults']['results']

    return [{
        'id_hotel': hotel['id'],
        'name': hotel['name'],
        'addres': hotel['address']['streetAddress'],
        'rating': hotel['starRating'],
        'price': hotel['ratePlan']['price']['current'],
        'location': hotel['landmarks']
    } for hotel in result]


async def filter_bestdeal(hotels, radius):
    return hotels
