from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_init import dp
from utils.botlogging import log_handler
from models import User
from config import SZ_COUNT_HOTEL
from hotelsrequests import search_locations
from fsmcash import StateBot


@dp.message_handler(state=StateBot.ENTER_CITY)
@log_handler
async def enter_city(message: types.Message, state: FSMContext):

    user = await User.from_message(message)
    citys = await search_locations(
        {'query': message.text,
         'locale': user.locale,
         'currency': user.currency}
    )

    if not isinstance(citys, dict):
        await state.finish()
        return await message.answer("Ошибка доступа к hotels.com.")

    if len(citys) == 0:
        return await message.answer(f"Город '{message.text}' не найден. Попробуйте еще раз.")

    if len(citys) == 1:
        async with state.proxy() as data:
            data['city_id'] = list(citys.keys())[0]
            data['city'] = list(citys.values())[0]

        return await switch_bot_request(message, state)

    async with state.proxy() as data:
        data['citys'] = citys

    markup = await get_markup_city(citys)
    await message.answer("Выберете город из списка:", reply_markup=markup)

    await StateBot.SELECT_CITY.set()


@dp.callback_query_handler(state=StateBot.SELECT_CITY)
@log_handler
async def select_city(call: types.CallbackQuery, state: FSMContext):

    async with state.proxy() as data:
        data['city_id'] = call.data
        data['city'] = data['citys'].get(call.data)

    await switch_bot_request(call.message, state)
    await call.message.delete()


async def get_markup_city(citys: dict) -> types.InlineKeyboardMarkup:

    markup = types.InlineKeyboardMarkup()
    for id_city, name_city in citys.items():
        markup.add(
            types.InlineKeyboardButton(name_city, callback_data=id_city)
        )
    return markup


async def switch_bot_request(message: types.Message, state: FSMContext):
    data = await state.get_data()
    request = data['request']

    match request:
        case '/lowprice' | '/highprice':
            await StateBot.ENTER_COUNT_HOTEL.set()
            await message.answer(f'Введите количество выводимых отелей(до {SZ_COUNT_HOTEL}):')

        case '/bestdeal':
            await StateBot.ENTER_PRICE.set()
            await message.answer('Введите диапозон цен через - ')
