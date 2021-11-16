from aiogram import types

from bot_init import dp
from utils.botlogging import log_handler
from models.user import User
from config import SZ_RADIUS, SZ_COUNT_HOTEL


@dp.message_handler(lambda message: User.from_message(message).next_hop == 'ENTER_PRICE')
@log_handler
async def enter_price(message: types.Message):
    temp = message.text.split('-')

    if len(temp) != 2 and all(value.strip().isdigit() for value in temp):
        return await message.answer('Некорректный ввод диапозона цен.\nПопробуйте еще раз.')

    user = User.from_message(message)

    begin_price, end_price = int(temp[0].strip()), int(temp[1].strip())
    user.set_item_dialog('begin_price', min(begin_price, end_price))
    user.set_item_dialog('end_price', max(begin_price, end_price))
    user.next_hop = 'ENTER_RADIUS'
    await message.answer(f'Введите удаленность от центра в км(до {SZ_RADIUS} км)')


@dp.message_handler(lambda message: User.from_message(message).next_hop == 'ENTER_RADIUS')
@log_handler
async def enter_radius(message: types.Message):

    if not message.text.isdigit():
        return await message.answer(f'({message.text}) - не число.\nПопробуйте еще раз.')

    if float(message.text) > SZ_RADIUS:
        return await message.answer(f'Максимальная удаленность от центра {SZ_RADIUS} км.\nПопробуйте еще раз.')

    user = User.from_message(message)
    user.set_item_dialog('radius', float(message.text))

    user.next_hop = 'ENTER_COUNT_HOTEL'
    await message.answer(f'Введите количество выводимых отелей(до {SZ_COUNT_HOTEL}):')
