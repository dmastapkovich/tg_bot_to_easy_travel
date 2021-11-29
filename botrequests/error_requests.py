from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from bot_init import dp
from config import INFO_COMMAND
from utils.botlogging import log_handler


@dp.message_handler()
@log_handler
async def cmd_error_hendler(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(f"Такой команды [{message.text}] нет в списке.\n"+INFO_COMMAND)
    await message.delete()
