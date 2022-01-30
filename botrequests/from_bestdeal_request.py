from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_init import dp, _
from config import SZ_RADIUS, SZ_COUNT_HOTEL
from utils import StateBot, log_handler


@dp.message_handler(state=StateBot.ENTER_PRICE)
@log_handler
async def enter_price(message: types.Message, state: FSMContext):
    temp = message.text.split('-')

    if len(temp) != 2 or not all(value.strip().isdigit() for value in temp):
        return await message.answer(
            '\n'.join(
                [
                    _('Некорректный ввод диапозона цен.'),
                    _('Попробуйте еще раз.')
                ]
            )
        )

    begin_price, end_price = int(temp[0].strip()), int(temp[1].strip())

    async with state.proxy() as data:
        data['begin_price'] = min(begin_price, end_price)
        data['end_price'] = max(begin_price, end_price)

    await StateBot.next()
    await message.answer(_('Введите удаленность от центра в км(до {text} км)').format(text=SZ_RADIUS))


@dp.message_handler(state=StateBot.ENTER_RADIUS)
@log_handler
async def enter_radius(message: types.Message, state: FSMContext):
    radius = message.text
    if ',' in radius:
        radius = radius.replace(',', '.', 1)
    if not radius.replace('.', '', 1).isdigit():
        return await message.answer(
            '\n'.join([
                _('({text}) - не число.').format(text=radius),
                _('Попробуйте еще раз.')
            ])
        )

    if float(radius) > SZ_RADIUS:
        return await message.answer(
            '\n'.join([
                _('Максимальная удаленность от центра {text} км.').format(text=SZ_RADIUS),
                _('Попробуйте еще раз.')
            ])
        )

    async with state.proxy() as data:
        data['radius'] = float(radius)

    await StateBot.next()
    await message.answer(_('Введите количество выводимых отелей(до {text}):').format(text=SZ_COUNT_HOTEL))
