from aiogram import types
from aiogram.dispatcher.filters import  CommandStart

from bot_init import dp
from utils.botlogging import log_handler


@dp.message_handler(CommandStart())
@log_handler
async def cmd_start(message: types.Message):
    await message.answer("Hello")
