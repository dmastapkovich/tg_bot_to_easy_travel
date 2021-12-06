from aiogram import types
from aiogram.dispatcher.filters import CommandHelp, CommandStart, CommandSettings
from aiogram.dispatcher import FSMContext


from bot_init import dp, _
from config import INFO_COMMAND, SETTINGS_CURR, SETTINGS_LOCALES
from models import User
from utils import StateBot, log_handler, locale_storage


@dp.message_handler(CommandHelp() | CommandStart(), state='*')
@log_handler
async def cmd_start_help(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('\n'.join([_(command) for command in INFO_COMMAND]))


@dp.message_handler(CommandSettings(), state='*')
@log_handler
async def cmd_settings(message: types.Message, state: FSMContext):
    await state.finish()

    user = await User.from_message(message)
    info: str = await get_settings(user)
    markup = await settings_mainmenu_markup()

    await message.answer(info, reply_markup=markup, parse_mode="Markdown")
    await message.delete()

    await StateBot.SETTINGS_OPTION_MENU.set()


@dp.callback_query_handler(state=StateBot.SETTINGS_OPTION_MENU)
@log_handler
async def cmd_option(callback: types.CallbackQuery, state: FSMContext):
    option = callback.data

    if option == 'cancel':
        await callback.message.delete()
        return await state.finish()

    async with state.proxy() as data:
        data['option'] = option

    if option == 'locale':
        markup = await option_markup(SETTINGS_LOCALES)
        await callback.message.edit_text(_("Выберите язык отображения сообщений от бота"))
        await callback.message.edit_reply_markup(markup)
    else:
        markup = await option_markup(SETTINGS_CURR)
        await callback.message.edit_text(_("Выберите удобную вам валюту."))
        await callback.message.edit_reply_markup(markup)

    await StateBot.COMMIT_SETTINGS.set()


@dp.callback_query_handler(state=StateBot.COMMIT_SETTINGS)
@log_handler
async def cmd_commit_settings(callback: types.CallbackQuery, state: FSMContext):
    commit_value = callback.data

    if commit_value == 'cancel':
        await callback.message.delete()
        return await state.finish()

    data = await state.get_data()
    user = await User.from_message(callback)

    await user.set_settings(option=data['option'], value=commit_value)

    if data['option'] == 'locale':
        await locale_storage.set(user.id_user, user.i18n_code)

    await callback.message.delete()
    await state.finish()


async def option_markup(option: dict[str, str]) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    markup.row(*[
        types.InlineKeyboardButton(value, callback_data=key) for key, value in option.items()
    ])
    markup.row(types.InlineKeyboardButton(
        _('Отменить'), callback_data='cancel'))
    return markup


async def settings_mainmenu_markup() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    blocale = types.InlineKeyboardButton(_('Язык'), callback_data='locale')
    bcurrency = types.InlineKeyboardButton(
        _('Валюта'), callback_data='currency')
    markup.row(blocale, bcurrency)
    markup.row(types.InlineKeyboardButton(
        _('Отменить'), callback_data='cancel'))
    return markup


async def get_settings(user: User) -> str:
    info = '\n'.join([
        _("Ваши текущие настройки:"),
        _("Язык отображения сообщений: *{text}*").format(
            text=SETTINGS_LOCALES.get(user.locale)),
        _("Используемая валюта: *{text}*").format(
            text=SETTINGS_CURR.get(user.currency)),
        _("Выберите опцию настройки:")
    ])
    return info
