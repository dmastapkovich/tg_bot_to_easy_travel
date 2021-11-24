from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_init import dp
from config import SZ_COUNT_PHOTO, SZ_COUNT_HOTEL
from fsmcash import StateBot
from models import User
from utils.botlogging import log_handler
from .check_request import print_check_request


@dp.message_handler(commands=['lowprice', 'highprice', 'bestdeal'], state='*')
@log_handler
async def command_search_hotel(message: types.Message, state: FSMContext):
    user = await User.from_message(message)
    await state.finish()
    async with state.proxy() as data:
        data['locale'] = user.locale
        data['currency'] = user.currency
        data['request'] = message.text

    await message.answer('Какой город хотите посетить?')
    await StateBot.ENTER_CITY.set()


@dp.message_handler(state=StateBot.ENTER_COUNT_HOTEL)
@log_handler
async def enter_count_hotel(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer(f'({message.text}) - не число.\nПопробуйте еще раз.')

    if int(message.text) > SZ_COUNT_HOTEL:
        return await message.answer(
            f'Можно вывести не больше {SZ_COUNT_HOTEL} отелей.\nПопробуйте еще раз.')

    async with state.proxy() as data:
        data['count_hotel'] = int(message.text)

    await StateBot.next()
    await message.answer('Выводить фотографии?',  reply_markup=get_yes_no_button())


@dp.callback_query_handler(state=StateBot.SELECT_PHOTO)
@log_handler
async def select_photo(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'no':
        await StateBot.CHECK_REQUEST.set()
        info_request = await print_check_request(state)
        await call.message.answer(f'Ваш запрос верен?\n{info_request}',
                                  reply_markup=get_yes_no_button())

    else:
        await StateBot.next()
        await call.message.answer(f'Введите количество выводимых фотографий(до {SZ_COUNT_PHOTO}):')

    await call.message.delete()


@dp.message_handler(state=StateBot.ENTER_COUNT_PHOTO)
@log_handler
async def enter_count_photo(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer(f'({message.text}) - не число.\nПопробуйте еще раз.')

    if int(message.text) > SZ_COUNT_PHOTO:
        return await message.answer(
            f'Можно вывести только {SZ_COUNT_PHOTO} фотографий.\nПопробуйте еще раз.')

    async with state.proxy() as data:
        data['count_photo'] = int(message.text)

    await StateBot.next()
    info_request = await print_check_request(state)
    await message.answer(f'Ваш запрос верен?\n{info_request}',
                         reply_markup=get_yes_no_button())


def get_yes_no_button() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton('Да', callback_data='yes')
    button_no = types.InlineKeyboardButton('Нет', callback_data='no')
    markup.row(button_yes, button_no)
    return markup
