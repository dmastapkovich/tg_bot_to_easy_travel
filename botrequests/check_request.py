from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types.input_media import MediaGroup, InputMediaPhoto
from aiogram.dispatcher import FSMContext

from bot_init import dp
from utils.botlogging import log_handler
from models.user import User
from hotelsrequests import get_hotels, get_photo_urls
from fsmcash import StateBot


@dp.callback_query_handler(state=StateBot.CHECK_REQUEST)
@log_handler
async def get_check_info(call: CallbackQuery, state: FSMContext):

    user = await User.from_message(call)
    data = await state.get_data()

    if call.data == 'yes':
        result = await get_hotels(data)
        hotels_info = await compose_info(result)

        await user.set_history(request=data, result=result)

        count_photo: int = data.get('count_photo')
        for id_hotel, hotel in hotels_info.items():
            if count_photo:
                photo_urls = await get_photo_urls(id_hotel, count_photo)
                media = await compose_media(photo_urls, hotel_info=hotel)
                await call.message.answer_media_group(media)
            else:
                await call.message.answer(hotel)

    await call.message.delete()
    await state.finish()


async def print_check_request(state: FSMContext) -> str:
    info = ''
    data = await state.get_data()
    for key, value in data.items():
        match key:
            case 'request':
                if value == '/lowprice':
                    info += 'Поиск дешевых отелей.\n'
                elif value == '/highprice':
                    info += 'Поиск дорогих отелей.\n'
                elif value == '/highprice':
                    info += 'Поиск отелей.\n'
            case 'begin_price':
                info += f'Цена от {value}\n'
            case 'end_price':
                info += f'Цена до {value}\n'
            case 'radius':
                info += f'Удаленность от центра до {value} км\n'
            case 'city':
                info += f'Город: {value}\n'
            case 'count_hotel':
                info += f'Количестов выводимых отелей: {value}\n'
            case 'count_photo':
                info += f'Количестов выводимых фотографий: {value}\n'
    return info


async def compose_info(hotels_result: list):
    info = {}
    for hotel in hotels_result:
        info[hotel['id_hotel']] = "\n".join([
            f"{hotel['name']}",
            f"Адрес: {hotel['addres']}",
            f"Рейтинг: {hotel['rating']}",
            f"Стоимость: {hotel['price']}",
            f"Удаленность:",
            *[f"{distance['label']} - {distance['distance']}" for distance in hotel['location']]
        ])
    return info


async def compose_media(photo_urls: list, hotel_info: str) -> MediaGroup:
    media: list[InputMediaPhoto] = []

    for url in photo_urls:
        media.append(InputMediaPhoto(url))
    media[0].caption = hotel_info

    return media
