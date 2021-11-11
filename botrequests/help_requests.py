from aiogram import types

from bot_init import dp
from utils.botlogging import log_handler


M = types.Message

@dp.message_handler(commands=['help'])
@log_handler
async def cmd_start(message: M):
    await message.answer("help")
