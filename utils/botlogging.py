import functools
from typing import ParamSpec, TypeVar, Callable

from aiogram import exceptions
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from loguru import logger

from config import LOGGER_FILE


# Type hinting
P = ParamSpec('P')
T = TypeVar('T')


def setup():
    logger.add(LOGGER_FILE, level="DEBUG", rotation="5 MB")
    logger.info(f"Setup loguru in: {LOGGER_FILE}")


def log_handler(func: Callable[P, T]) -> Callable[P, T]:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Callable[P, T]:
        result = ''
        if isinstance(args[0], types.Message):
            result = args[0].text
        if isinstance(args[0], types.CallbackQuery):
            result = args[0].data
            
        state:FSMContext = kwargs['state']
        user = f"User @{args[0].from_user.username} [id{args[0].from_user.id}]"

        try:
            logger.info(f"{user} event function [{func.__name__}]. Entered value: {result}")
            return await func(*args, **kwargs)
        
        except exceptions.BadRequest as error:
            logger.exception(
                f"[{error.__class__.__name__} -> {error}] {user} event function [{func.__name__}].")

        except exceptions.BotBlocked as error:
            logger.error(f"[{error.__class__.__name__} -> {error}] {user}")
            await state.finish()
        
    return logger.catch(wrapper)
