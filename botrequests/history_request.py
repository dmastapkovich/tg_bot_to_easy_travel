from aiogram import types

from bot_init import dp
from utils.botlogging import log_handler
from models.user import User


@dp.message_handler(commands=['history'])
@log_handler
async def cmd_history(message: types.Message):
    user: User = User.from_message(message)
    history: list = user.get_history()
    for value in history:
        await message.reply(value)
        
    
    
