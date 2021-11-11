from typing import ParamSpec, TypeVar, Callable
from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher


from .config import *

from .botlogging import logging, logger


# Type hinting
P = ParamSpec('P')
T = TypeVar('T')
M = types.Message
C = types.CallbackQuery
IKM = types.InlineKeyboardMarkup


# Initialization Telegram bot
bot = Bot(token=TOKEN)
disp = Dispatcher(bot)
disp.middleware.setup(LoggingMiddleware())


# initialization command
from .botrequests.start_help_requests import command_start


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    logger.warning('Shutting down..')

    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()

    logger.warning('Bye!')


# @disp.message_handler(commands=['history'])
# @logging
# async def command_start(message: M):
#     await message.answer('it work')


# @disp.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
# @logging
# async def command_search_hotel(message: M):

#     user = User.from_message(message)
#     user.bot_request = message.text

#     await message.answer('Какой город хотите посетить?')

#     user.next_hop = 'ENTER_CITY'


# @disp.message_handler(func=lambda message: User.from_message(message).next_hop == 'ENTER_CITY')
# @logging
# async def enter_city(message: M):

#     user = User.from_message(message)

#     match user.bot_request:
#         case '/lowprice' | '/highprice':
#             user.next_hop = 'ENTER_COUNT_HOTEL'
#             await message.answer('Введите количество выводимых отелей(до 5):')

#         case '/bestdeal':
#             user.next_hop = 'ENTER_PRICE'
#             await message.answer('Введите диапозон цен через - ')


# @disp.message_handler(func=lambda message: User.from_message(message).next_hop == 'ENTER_PRICE')
# @logging
# async def enter_price(message: M):
#     temp = message.text.split('-')

#     if len(temp) != 2 and all(value.strip().isdigit() for value in temp):
#         raise TypeError(
#             'Некорректный ввод диапозона цен.\nВведите стоимость еще раз')
#     else:
#         begin_price, end_price = int(temp[0].strip()), int(temp[1].strip())
#         user_request['begin_price'] = min(begin_price, end_price)
#         user_request['end_price'] = max(begin_price, end_price)

#         user_dialog[message.chat.id] = 'ENTER_RADIUS'
#         bot.send_message(message.chat.id,
#                          'Введите удаленность от центра в км(до 5км)')


# @disp.message_handler(func=lambda message: user_dialog.get(message.chat.id) == 'ENTER_RADIUS')
# @logging
# def enter_radius(message: M):

#     if not message.text.isdigit():
#         raise TypeError('Вы ввели не число')

#     if float(message.text) > 5.01:
#         raise ValueError('Максимальная удаленность от центра 10 км')

#     user_request['radius'] = float(message.text)

#     user_dialog[message.chat.id] = 'ENTER_COUNT_HOTEL'
#     bot.send_message(
#         message.chat.id, 'Введите количество выводимых отелей(до 5):')


# @disp.message_handler(func=lambda message: user_dialog.get(message.chat.id) == 'ENTER_COUNT_HOTEL')
# @logging
# def enter_count_hotel(message: M):

#     if not message.text.isdigit():
#         raise TypeError('Вы ввели не число')

#     if int(message.text) > 5:
#         raise ValueError('Можно вывести только 5 отелей')

#     user_request['count_hotel'] = int(message.text)

#     user_dialog[message.chat.id] = 'SELECT_PHOTO'
#     bot.send_message(message.chat.id, 'Выводить фотографии?',
#                      reply_markup=get_yes_no_button())


# @disp.callback_query_handler(func=lambda call: user_dialog.get(call.message.chat.id) == 'SELECT_PHOTO')
# @logging
# def select_photo(call: C):

#     bot.delete_message(call.message.chat.id, call.message.id)

#     if call.data == 'no':
#         user_dialog[call.message.chat.id] = 'CHECK_REQUEST'
#         bot.send_message(call.message.chat.id,
#                          f'Ваш запрос верен?\n{print_info()}',
#                          reply_markup=get_yes_no_button())

#     else:
#         user_dialog[call.message.chat.id] = 'ENTER_COUNT_PHOTO'
#         bot.send_message(call.message.chat.id,
#                          'Введите количество выводимых фотографий(до 5):')


# @disp.message_handler(func=lambda message: user_dialog.get(message.chat.id) == 'ENTER_COUNT_PHOTO')
# @logging
# def enter_count_photo(message: M):

#     if not message.text.isdigit():
#         raise TypeError('Вы ввели не число')

#     if int(message.text) > 5:
#         raise ValueError('Можно вывести только 5 фотографий')

#     user_request['count_photo'] = int(message.text)

#     user_dialog[message.chat.id] = 'CHECK_REQUEST'
#     bot.send_message(message.chat.id,
#                      f'Ваш запрос верен?\n{print_info()}',
#                      reply_markup=get_yes_no_button())


# @disp.callback_query_handler(func=lambda call: user_dialog.get(call.message.chat.id) == 'CHECK_REQUEST')
# @logging
# def get_check_info(call: C):
#     bot.answer_callback_query(call.id, text='Ждите ответа')
#     bot.delete_message(call.message.chat.id, call.message.id)
#     if call.data == 'yes':
#         print(user_request)


# def print_info() -> str:
#     info = ''
#     for key, value in user_request.items():
#         match key:
#             case 'request':
#                 if value == '/lowprice':
#                     info += 'Поиск дешевых отелей.\n'
#                 elif value == '/highprice':
#                     info += 'Поиск дорогих отелей.\n'
#                 elif value == '/highprice':
#                     info += 'Поиск отелей.\n'
#             case 'begin_price':
#                 info += f'Цена от {value}\n'
#             case 'end_price':
#                 info += f'Цена до {value}\n'
#             case 'radius':
#                 info += f'Удаленность от центра до {value} км\n'
#             case 'city':
#                 info += f'Город: {value}\n'
#             case 'count_hotel':
#                 info += f'Количестов выводимых отелей: {value}\n'
#             case 'count_photo':
#                 info += f'Количестов выводимых фотографий: {value}\n'
#     return info


# def get_yes_no_button() -> IKM:
#     markup = types.InlineKeyboardMarkup()
#     button_yes = types.InlineKeyboardButton('Да', callback_data='yes')
#     button_no = types.InlineKeyboardButton('Нет', callback_data='no')
#     markup.row(button_yes, button_no)
#     return markup


# def get_user(message: M):
#     # select in db
#     return User.from_message(message)
