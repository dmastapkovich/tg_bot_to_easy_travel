from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_init import dp
from utils.botlogging import log_handler
from config import SZ_RADIUS, SZ_COUNT_HOTEL
from fsmcash import StateBot


@dp.message_handler(state=StateBot.ENTER_PRICE)
@log_handler
async def enter_price(message: types.Message, state: FSMContext):
    temp = message.text.split('-')

    if len(temp) != 2 and all(value.strip().isdigit() for value in temp):
        return await message.answer('Некорректный ввод диапозона цен.\nПопробуйте еще раз.')

    begin_price, end_price = int(temp[0].strip()), int(temp[1].strip())

    async with state.proxy() as data:
        data['begin_price'] = min(begin_price, end_price)
        data['end_price'] = max(begin_price, end_price)

    await StateBot.next()
    await message.answer(f'Введите удаленность от центра в км(до {SZ_RADIUS} км)')


@dp.message_handler(state=StateBot.ENTER_RADIUS)
@log_handler
async def enter_radius(message: types.Message, state: FSMContext):

    if not message.text.isdigit():
        return await message.answer(f'({message.text}) - не число.\nПопробуйте еще раз.')

    if float(message.text) > SZ_RADIUS:
        return await message.answer(f'Максимальная удаленность от центра {SZ_RADIUS} км.\nПопробуйте еще раз.')

    async with state.proxy() as data:
        data['radius'] = float(message.text)

    await StateBot.next()
    await message.answer(f'Введите количество выводимых отелей(до {SZ_COUNT_HOTEL}):')
