from aiogram import types
from aiogram.utils.markdown import hlink

from bot_init import dp
from models.user import User, History
from utils.botlogging import log_handler


@dp.message_handler(commands=['history'])
@log_handler
async def cmd_history(message: types.Message):
    user: User = await User.from_message(message)
    history: list[History] = await user.get_history()
    for value in history:
        info = await compose_history(value)
        await message.reply(info, parse_mode='HTML', disable_web_page_preview=True)


async def compose_history(history: History) -> str:
    info = [f"Время: {history.time_request.strftime('%H:%M %Y-%m-%d')}"]
    
    req = history.request
    curr = req['currency']
    if req['request'] == '/lowprice':
        info.append(
            f"Поиск дешевых отелей в городе {req['city']}:"
        )
    elif req['request'] == '/highprice':
        info.append(
            f"Поиск дорогих отелей в городе {req['city']}:"
        )
    else:
        info.extend([
            f"Поиск отелей в городе {req['city']}",
            f"Удаленность до центра города до {req['radius']}",
            f"Стоимостью от {req['begin_price']} {curr} до {req['end_price']} {curr}"
        ])
        
    info.append('Результат поиска:')
    
    hotels: list[dict] = history.result
    for index, hotel in enumerate(hotels, start=1):
        hotel_info = [
            f"{index}. {hlink(hotel['name'], hotel['url_hotel'])}.",
            f"Рейтинг {hotel['rating']}.",
            f"Стоимость {hotel['price']}.",
        ]
        info.append(
            ' '.join(hotel_info)
        )
        
    return '\n'.join(info)