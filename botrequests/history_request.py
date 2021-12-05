from aiogram import types
from aiogram.utils.markdown import hlink

from bot_init import dp, _
from models import User, History
from utils import log_handler


@dp.message_handler(commands=['history'])
@log_handler
async def cmd_history(message: types.Message):
    user: User = await User.from_message(message)
    history: list[History] = await user.get_history()
    for value in history:
        info = await compose_history(value)
        await message.reply(info, parse_mode='HTML', disable_web_page_preview=True)


async def compose_history(history: History) -> str:
    info = [_("Время: {text}").format(text=history.time_request.strftime('%H:%M %Y-%m-%d'))]

    req = history.request
    curr = req['currency']
    if req['request'] == '/lowprice':
        info.append(
            _("Поиск дешевых отелей в городе {text}:").format(text=req['city'])
        )
    elif req['request'] == '/highprice':
        info.append(
            _("Поиск дорогих отелей в городе {text}:").format(text=req['city'])
        )
    else:
        info.extend([
            _("Поиск отелей в городе {text}:").format(text=req['city']),
            _("Удаленность до центра города до {text}:").format(text=req['radius']),
            _("Стоимостью от {text_1} {curr} до {text_2} {curr}").format(
                text_1=req['begin_price'],
                text_2=req['end_price'],
                curr=curr
            )
        ])

    info.append('Результат поиска:')

    hotels: list[dict] = history.result
    for index, hotel in enumerate(hotels, start=1):
        hotel_info = [
            "{index}) {text}.".foramt(index=index, text=hlink(hotel['name'], hotel['url_hotel'])),
            _("Рейтинг {text}.").format(text=hotel['rating']),
            _("Стоимость {text}.").format(text=hotel['price']),
        ]
        info.append(
            ' '.join(hotel_info)
        )

    return '\n'.join(info)
