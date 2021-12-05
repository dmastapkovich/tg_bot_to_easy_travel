import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram_calendar import simple_cal_callback, SimpleCalendar

from bot_init import dp, _
from config import SZ_COUNT_PHOTO, SZ_COUNT_HOTEL
from models import User
from utils import StateBot, log_handler
from .check_request import print_check_request


@dp.message_handler(commands=['lowprice', 'highprice', 'bestdeal'], state='*')
@log_handler
async def command_search_hotel(message: types.Message, state: FSMContext):
    user = await User.from_message(message)
    await state.finish()
    async with state.proxy() as data:
        data['locale'] = user.locale
        data['currency'] = user.currency
        data['request'] = message.text

    await message.answer(_('Какой город хотите посетить?'))
    await StateBot.ENTER_CITY.set()


@dp.callback_query_handler(simple_cal_callback.filter(), state=StateBot.SELECT_DATE_IN)
@log_handler
async def process_simple_calendar(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(call, callback_data)
    if selected:
        async with state.proxy() as data:
            data['checkIn'] = date
        await StateBot.SELECT_DATE_OUT.set()
        await call.message.answer(_('Выберите дату выезда:'), reply_markup=await SimpleCalendar().start_calendar())
        await call.message.delete()


@dp.callback_query_handler(simple_cal_callback.filter(), state=StateBot.SELECT_DATE_OUT)
@log_handler
async def process_simple_calendar(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(call, callback_data)
    if selected:
        async with state.proxy() as data:
            data['checkOut'] = date
       
        validate = await validate_date(data['checkIn'], data['checkOut'], state)
        
        data = await state.get_data()
        if not validate:
            await call.message.answer(_('\n'.join(
                [
                    _('Некорректный ввод даты'),
                    _('Автоматически установлены:'),
                    _('Дата заезда: {value}').format(value=data['checkIn']),
                    _('Дата выезда: {value}').format(value=data['checkOut'])
                ]
            )))
        
        match data['request']:
            case '/lowprice' | '/highprice':
                await StateBot.ENTER_COUNT_HOTEL.set()
                await call.message.answer(_('Введите количество выводимых отелей(до {text}):').format(text=SZ_COUNT_HOTEL))

            case '/bestdeal':
                await StateBot.ENTER_PRICE.set()
                await call.message.answer(_('Введите диапозон цен через - '))

        await call.message.delete()


async def validate_date(dateIn, dateOut, state:FSMContext) -> bool:
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    
    check = True
    if today > dateIn:
        async with state.proxy() as data:
            data['checkIn'] = today     
        check = False   
    
    if tomorrow > dateOut:
        async with state.proxy() as data:
            data['checkOut'] = tomorrow
        check = False 
    
    return check


@dp.message_handler(state=StateBot.ENTER_COUNT_HOTEL)
@log_handler
async def enter_count_hotel(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer(
            '\n'.join(
                [
                    _('({text}) - не число.').format(text=message.text),
                    _('Попробуйте еще раз.')
                ]
            )
        )

    if int(message.text) > SZ_COUNT_HOTEL:
        return await message.answer(
            '\n'.join(
                [
                    _('Можно вывести не больше {text} отелей.').format(
                        text=SZ_COUNT_HOTEL),
                    _('Попробуйте еще раз.')
                ]
            )
        )

    async with state.proxy() as data:
        data['count_hotel'] = int(message.text)

    await StateBot.next()
    await message.answer(_('Выводить фотографии?'),  reply_markup=get_yes_no_button())


@dp.callback_query_handler(state=StateBot.SELECT_PHOTO)
@log_handler
async def select_photo(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'no':
        await StateBot.CHECK_REQUEST.set()
        info_request = await print_check_request(state)
        await call.message.answer(
            '\n'.join(
                [
                    _('Ваш запрос верен?'),
                    info_request
                ]
            ),
            reply_markup=get_yes_no_button()
        )

    else:
        await StateBot.next()
        await call.message.answer(
            _('Введите количество выводимых фотографий(до {text}):').format(
                text=SZ_COUNT_PHOTO)
        )

    await call.message.delete()


@dp.message_handler(state=StateBot.ENTER_COUNT_PHOTO)
@log_handler
async def enter_count_photo(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer(
            '\n'.join(
                [
                    _('({text}) - не число.').format(text=message.text),
                    'Попробуйте еще раз.'
                ]
            )
        )

    if int(message.text) > SZ_COUNT_PHOTO:
        return await message.answer(
            '\n'.join(
                [
                    _('Можно вывести не больше {text} фотографий.').format(
                        text=SZ_COUNT_PHOTO),
                    _('Попробуйте еще раз.')
                ]
            )
        )

    async with state.proxy() as data:
        data['count_photo'] = int(message.text)

    await StateBot.next()
    info_request = await print_check_request(state)
    await message.answer(
        '\n'.join(
            [
                _('Ваш запрос верен?'),
                info_request
            ]
        ),
        reply_markup=get_yes_no_button()
    )


def get_yes_no_button() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(_('Да'), callback_data='yes')
    button_no = types.InlineKeyboardButton(_('Нет'), callback_data='no')
    markup.row(button_yes, button_no)
    return markup
