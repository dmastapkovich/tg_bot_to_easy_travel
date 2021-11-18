import json

from aiogram import types

from bot_init import dp
from utils.botlogging import log_handler
from models.user import User
from config import SZ_COUNT_HOTEL
from utils.hotels_requests import search_locations


@dp.message_handler(lambda message: User.from_message(message).next_hop == 'ENTER_CITY')
@log_handler
async def enter_city(message: types.Message):

    user = User.from_message(message)
    citys = await search_locations(
        {'query': message.text,
         'locale': user.locale,
         'currency': user.currency}
    )

    if not isinstance(citys, dict):
        user.next_hop = ''
        return await message.answer("Ошибка доступа к hotels.com.")

    if len(citys) == 0:
        return await message.answer(f"Город '{message.text}' не найден. Попробуйте еще раз.")

    if len(citys) == 1:
        user.set_item_dialog('city', citys.values()[0])
        await switch_bot_request(message, user)

    markup = await get_markup_city(citys)
    user.set_item_dialog('city', json.dumps(citys))
    await message.answer("Выберете город из списка:", reply_markup=markup)
    user.next_hop = 'SELECT_CITY'


@dp.callback_query_handler(lambda message: User.from_message(message).next_hop == 'SELECT_CITY')
@log_handler
async def select_city(call: types.CallbackQuery):

    user = User.from_message(call)

    user.set_item_dialog('city_id', call.data)
    user.set_item_dialog('city', json.loads(
        user.dialog.get('city'))[call.data])

    await switch_bot_request(call.message, user)
    await call.message.delete()


async def get_markup_city(citys: dict) -> types.InlineKeyboardMarkup:

    markup = types.InlineKeyboardMarkup()
    for id_city, name_city in citys.items():
        markup.add(
            types.InlineKeyboardButton(name_city, callback_data=id_city)
        )
    return markup


async def switch_bot_request(message: types.Message, user):
    match user.bot_request:
        case '/lowprice' | '/highprice':
            user.next_hop = 'ENTER_COUNT_HOTEL'
            await message.answer(f'Введите количество выводимых отелей(до {SZ_COUNT_HOTEL}):')

        case '/bestdeal':
            user.next_hop = 'ENTER_PRICE'
            await message.answer('Введите диапозон цен через - ')
