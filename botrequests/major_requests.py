from aiogram import types

from bot_init import dp
from utils.botlogging import log_handler
from models.user import User


M = types.Message

@dp.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
@log_handler
async def command_search_hotel(message: M):

    user = User.from_message(message)
    user.bot_request = message.text

    await message.answer('Какой город хотите посетить?')

    user.next_hop = 'ENTER_CITY'


@dp.message_handler(lambda message: User.from_message(message).next_hop == 'ENTER_CITY')
@log_handler
async def enter_city(message: M):

    user = User.from_message(message)

    match user.bot_request:
        case '/lowprice' | '/highprice':
            user.next_hop = 'ENTER_COUNT_HOTEL'
            await message.answer('Введите количество выводимых отелей(до 5):')

        case '/bestdeal':
            user.next_hop = 'ENTER_PRICE'
            await message.answer('Введите диапозон цен через - ')