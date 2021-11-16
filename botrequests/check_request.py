from aiogram import types

from bot_init import dp
from utils.botlogging import log_handler
from models.user import User


@dp.callback_query_handler(lambda message: User.from_message(message).next_hop == 'CHECK_REQUEST')
@log_handler
async def get_check_info(call: types.CallbackQuery):
    await call.message.delete()
    user = User.from_message(call)
    if call.data == 'yes':
        user.set_history_request()
        print(user.dialog)


def print_info(user: User) -> str:
    info = ''
    for key, value in user.dialog.items():
        match key:
            case 'request':
                if value == '/lowprice':
                    info += 'Поиск дешевых отелей.\n'
                elif value == '/highprice':
                    info += 'Поиск дорогих отелей.\n'
                elif value == '/highprice':
                    info += 'Поиск отелей.\n'
            case 'begin_price':
                info += f'Цена от {value}\n'
            case 'end_price':
                info += f'Цена до {value}\n'
            case 'radius':
                info += f'Удаленность от центра до {value} км\n'
            case 'city':
                info += f'Город: {value}\n'
            case 'count_hotel':
                info += f'Количестов выводимых отелей: {value}\n'
            case 'count_photo':
                info += f'Количестов выводимых фотографий: {value}\n'
    return info
