from aiogram import types

from bot_init import dp
from utils.botlogging import log_handler
from models.user import User

@dp.message_handler(commands=['start'])
@log_handler
async def cmd_start(message: types.Message):
    
    user = await User.from_message(message)
    await message.answer("start")
    
