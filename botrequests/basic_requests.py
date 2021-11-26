from aiogram import types
from aiogram.dispatcher.filters import CommandHelp, CommandStart, CommandSettings
from aiogram.dispatcher import FSMContext


from bot_init import dp
from config import INFO_COMMAND, SETTINGS_CURR, SETTINGS_LOCALES
from fsmcash import StateBot
from models import User
from utils.botlogging import log_handler


@dp.message_handler(CommandHelp() | CommandStart(), state='*')
@log_handler
async def cmd_start_help(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(INFO_COMMAND)


@dp.message_handler(CommandSettings(), state='*')
@log_handler
async def cmd_settings(message: types.Message, state: FSMContext):
    await state.finish()

    user = await User.from_message(message)
    info = await user.get_settings()
    markup = await settings_mainmenu_markup()

    await message.answer(info, reply_markup=markup, parse_mode="Markdown")
    await message.delete()

    await StateBot.SETTINGS_OPTION_MENU.set()


@dp.callback_query_handler(state=StateBot.SETTINGS_OPTION_MENU)
@log_handler
async def cmd_option(callback: types.CallbackQuery, state: FSMContext):
    option = callback.data

    async with state.proxy() as data:
        data['option'] = option

    if option == 'locale':
        markup = await option_markup(SETTINGS_LOCALES)
        await callback.message.edit_text("Выберите язык отображения сообщений от бота")
        await callback.message.edit_reply_markup(markup)
    else:
        markup = await option_markup(SETTINGS_CURR)
        await callback.message.edit_text("Выберите удобную вам валюту.")
        await callback.message.edit_reply_markup(markup)

    await StateBot.COMMIT_SETTINGS.set()


@dp.callback_query_handler(state=StateBot.COMMIT_SETTINGS)
@log_handler
async def cmd_commit_settings(callback: types.CallbackQuery, state: FSMContext):
    commit_value = callback.data

    data = await state.get_data()
    user = await User.from_message(callback)

    await user.set_settings(option=data['option'], value=commit_value)
    await callback.message.delete()
    await state.finish()


async def option_markup(option: dict[str, str]) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    markup.row(*[
        types.InlineKeyboardButton(value, callback_data=key) for key, value in option.items()
    ])
    return markup


async def settings_mainmenu_markup() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    blocale = types.InlineKeyboardButton('Язык', callback_data='locale')
    bcurrency = types.InlineKeyboardButton('Валюта', callback_data='currency')
    markup.row(blocale, bcurrency)
    return markup
