from aiogram import types

from bot_init import dp
from utils.botlogging import log_handler


@dp.message_handler(commands=['start'])
@log_handler
async def cmd_start(message: types.Message):
    await message.answer("start")
