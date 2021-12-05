from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from bot_init import dp, _
from config import INFO_COMMAND
from utils import log_handler


@dp.message_handler()
@log_handler
async def cmd_error_hendler(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(
        '\n'.join(
            [
                _("Такой команды [{text}] нет в списке.").format(text=message.text),
                INFO_COMMAND
            ]
        )
    )
    await message.delete()
