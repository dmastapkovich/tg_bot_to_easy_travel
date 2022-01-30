from datetime import datetime
from aiogram.types import CallbackQuery, Message
from aiogram.types.input_media import MediaGroup, InputMediaPhoto
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink
from aiogram.utils.exceptions import BadRequest
from loguru import logger

from bot_init import dp, _
from config import HOTELS_URL, SETTINGS_CURR
from hotelsrequests import get_hotels, get_photo_urls
from models import User
from utils import StateBot, log_handler


@dp.callback_query_handler(state=StateBot.CHECK_REQUEST)
@log_handler
async def get_check_info(call: CallbackQuery, state: FSMContext):
    user = await User.from_message(call)
    data = await state.get_data()

    if call.data == 'yes':
        info_await: Message = await call.message.answer(_('Ожидайте. Уже идет поиск отелей...'))

        result = await get_hotels(data)
        if not isinstance(result, list):
            await call.message.answer(_("Ошибка доступа к {text}").format(text=HOTELS_URL))
            await call.message.delete()
            return await state.finish()

        size_result = len(result)
        if size_result == 0:
            await call.message.reply(_('К сожалению, Мы не смогли найти для Вас отели по вашему запросу.'))
            await state.finish()
            await info_await.delete()
            return await call.message.delete()

        if size_result != int(data['count_hotel']):
            await call.message.answer(_('По вашему запросу было найдено только {text} отеля.').format(text=size_result))

        await info_await.delete()
        hotels_info = await compose_info(result, data)
        await user.set_history(request=data, result=result)

        count_photo: int = data.get('count_photo')
        for id_hotel, hotel in hotels_info.items():
            if count_photo:
                photo_urls = await get_photo_urls(id_hotel, count_photo)

                if photo_urls is None:
                    await call.message.answer(_("Ошибка доступа к фотографиям {text}").format(text=HOTELS_URL))
                    await call.message.answer(hotel, parse_mode='HTML', disable_web_page_preview=True)
                    continue

                media = await compose_media(photo_urls, hotel_info=hotel)
                try:
                    await call.message.answer_media_group(media)
                except BadRequest as error:
                    logger.exception(
                        f"[{error.__class__.__name__} -> {error}] {user}")
                    await call.message.answer(_("Ошибка вывода фотографий."))
                    await call.message.answer(hotel, parse_mode='HTML', disable_web_page_preview=True)
            else:
                await call.message.answer(hotel, parse_mode='HTML', disable_web_page_preview=True)

    await call.message.delete()
    await state.finish()


async def print_check_request(state: FSMContext, curr:str) -> str:
    info = []
    data = await state.get_data()
    for key, value in data.items():
        match key:
            case 'request':
                if value == '/lowprice':
                    info.append(_('Поиск дешевых отелей.'))
                elif value == '/highprice':
                    info.append(_('Поиск дорогих отелей.'))
                elif value == '/highprice':
                    info.append(_('Поиск отелей.'))
            case 'checkIn':
                temp_date = datetime.strptime(value, '%Y-%m-%d').strftime('%d.%m.%Y')
                info.append(_('Дата заезда: {value}').format(value=temp_date))
            case 'checkOut':
                temp_date = datetime.strptime(value, '%Y-%m-%d').strftime('%d.%m.%Y')
                info.append(_('Дата выезда: {value}').format(value=temp_date))
            case 'begin_price':
                info.append(_('Цена за сутки от {value}').format(value=f'{value} {SETTINGS_CURR[curr]}'))
            case 'end_price':
                info.append(_('Цена за сутки до {value}').format(value=f'{value} {SETTINGS_CURR[curr]}'))
            case 'radius':
                info.append(
                    _('Удаленность от центра до {value} км').format(value=value))
            case 'city':
                info.append(_('Город: {value}').format(value=value))
            case 'count_hotel':
                info.append(
                    _('Количестов выводимых отелей: {value}').format(value=value))
            case 'count_photo':
                info.append(
                    _('Количестов выводимых фотографий: {value}').format(value=value))
    return '\n'.join(info)


async def compose_info(hotels_result: list, data: dict) -> dict[int, list]:
    info = {}
    for hotel in hotels_result:
        checkIn = datetime.strptime(data['checkIn'], '%Y-%m-%d').strftime('%d.%m.%Y')
        checkOut = datetime.strptime(data['checkOut'], '%Y-%m-%d').strftime('%d.%m.%Y')
        info[hotel['id_hotel']] = "\n".join([
            hlink(hotel['name'], hotel['url_hotel']),
            _("Адрес: {text}").format(text=hotel['addres']),
            # _("Рейтинг: {text}").format(text=hotel['rating']),
            _("Дата заезда: {date_in}").format(date_in=checkIn),
            _("Дата выезда: {date_out}").format(date_out=checkOut),
            _("Стоимость: {text}").format(text=hotel['price']),
            _("Удаленность:"),
            *[f"{distance['label']} - {distance['distance']}" for distance in hotel['location']]
        ])
    return info


async def compose_media(photo_urls: list, hotel_info: str) -> MediaGroup:
    media: list[InputMediaPhoto] = []

    for url in photo_urls:
        media.append(InputMediaPhoto(url))

    media[0].caption = hotel_info
    media[0].parse_mode = 'HTML'

    return media
