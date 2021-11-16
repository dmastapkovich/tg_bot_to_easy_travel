from aiogram import types

from .check_request import print_info
from bot_init import dp
from utils.botlogging import log_handler
from models.user import User
from config import SZ_COUNT_PHOTO, SZ_COUNT_HOTEL


@dp.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
@log_handler
async def command_search_hotel(message: types.Message):

    user = User.from_message(message)
    user.bot_request = message.text
    user.set_item_dialog('request', message.text)

    await message.answer('Какой город хотите посетить?')

    user.next_hop = 'ENTER_CITY'


# @dp.message_handler(lambda message: User.from_message(message).next_hop == 'ENTER_CITY')
# @log_handler
# async def enter_city(message: types.Message):

#     user = User.from_message(message)
#     user.set_item_dialog('city', message.text)

#     match user.bot_request:
#         case '/lowprice' | '/highprice':
#             user.next_hop = 'ENTER_COUNT_HOTEL'
#             await message.answer(f'Введите количество выводимых отелей(до {SZ_COUNT_HOTEL}):')

#         case '/bestdeal':
#             user.next_hop = 'ENTER_PRICE'
#             await message.answer('Введите диапозон цен через - ')


@dp.message_handler(lambda message: User.from_message(message).next_hop == 'ENTER_COUNT_HOTEL')
@log_handler
async def enter_count_hotel(message: types.Message):

    if not message.text.isdigit():
        await message.answer(f'({message.text}) - не число.\nПопробуйте еще раз.')
        return

    if int(message.text) > SZ_COUNT_HOTEL:
        raise ValueError(
            f'Можно вывести не больше {SZ_COUNT_HOTEL} отелей.\nПопробуйте еще раз.')

    user = User.from_message(message)
    
    user.set_item_dialog('count_hotel', int(message.text))
    user.next_hop = 'SELECT_PHOTO'

    await message.answer('Выводить фотографии?',  reply_markup=get_yes_no_button())


@dp.callback_query_handler(lambda message: User.from_message(message).next_hop == 'SELECT_PHOTO')
@log_handler
async def select_photo(call: types.CallbackQuery):

    await call.message.delete()
    user = User.from_message(call)
    if call.data == 'no':
        user.next_hop = 'CHECK_REQUEST'
        await call.message.answer(f'Ваш запрос верен?\n{print_info(user)}',
                                  reply_markup=get_yes_no_button())

    else:
        user.next_hop = 'ENTER_COUNT_PHOTO'
        await call.message.answer(f'Введите количество выводимых фотографий(до {SZ_COUNT_PHOTO}):')


@dp.message_handler(lambda message: User.from_message(message).next_hop == 'ENTER_COUNT_PHOTO')
@log_handler
async def enter_count_photo(message: types.Message):

    if not message.text.isdigit():
        raise TypeError(f'({message.text}) - не число.\nПопробуйте еще раз.')

    if int(message.text) > SZ_COUNT_PHOTO:
        raise ValueError(
            f'Можно вывести только {SZ_COUNT_PHOTO} фотографий.\nПопробуйте еще раз.')

    user = User.from_message(message)
    user.set_item_dialog('count_photo', int(message.text))

    user.next_hop = 'CHECK_REQUEST'
    await message.answer(f'Ваш запрос верен?\n{print_info(user)}',
                         reply_markup=get_yes_no_button())


def get_yes_no_button() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton('Да', callback_data='yes')
    button_no = types.InlineKeyboardButton('Нет', callback_data='no')
    markup.row(button_yes, button_no)
    return markup
