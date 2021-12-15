from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram_calendar import SimpleCalendar

from bot_init import dp, _
from config import HOTELS_URL
from hotelsrequests import search_locations
from models import User
from utils import StateBot, log_handler, set_city, get_city_request


@dp.message_handler(state=StateBot.ENTER_CITY)
@log_handler
async def enter_city(message: types.Message, state: FSMContext):
    user: User = await User.from_message(message)
    cities: str | list[str] = await get_city_request(message.text)

    if not cities:
        cities = await search_locations(
            {'query': message.text,
             'locale': user.locale,
             'currency': user.currency}
        )

        if not isinstance(cities, dict):
            await state.finish()
            return await message.answer(_("Ошибка доступа к {text}").format(text=HOTELS_URL))

        if len(cities) == 0:
            return await message.answer(_("Город '{text}' не найден. Попробуйте сменить локализацию или раскладку.").format(text=message.text))

        await set_city(message.text, cities)

    if len(cities) == 1:
        async with state.proxy() as data:
            data['city_id'] = list(cities.keys())[0]
            data['city'] = list(cities.values())[0]
        await StateBot.SELECT_DATE_IN.set()
        return await message.answer(_('Выберите дату заезда:'), reply_markup=await SimpleCalendar().start_calendar())

    async with state.proxy() as data:
        data['cities'] = cities

    markup = await get_markup_city(cities)
    await message.answer(_("Выберете город из списка:"), reply_markup=markup)
    await StateBot.SELECT_CITY.set()


@dp.callback_query_handler(state=StateBot.SELECT_CITY)
@log_handler
async def select_city(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['city_id'] = call.data
        data['city'] = data['cities'].get(call.data)

    await StateBot.SELECT_DATE_IN.set()
    await call.message.answer(_('Выберите дату заезда:'), reply_markup=await SimpleCalendar().start_calendar())
    await call.message.delete()


async def get_markup_city(cities: dict) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    for id_city, name_city in cities.items():
        markup.add(
            types.InlineKeyboardButton(name_city, callback_data=id_city)
        )
    return markup
