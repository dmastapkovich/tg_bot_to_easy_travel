import functools
from typing import ParamSpec, TypeVar, Callable

from aiogram import types
from loguru import logger

from config import LOGGER_FILE


# Type hinting
P = ParamSpec('P')
T = TypeVar('T')


def setup():
    logger.level('INFO')
    logger.add(LOGGER_FILE, level="INFO", rotation="5 MB")
    logger.info(f"Setup loguru in: {LOGGER_FILE}")


def log_handler(func: Callable[P, T]) -> Callable[P, T]:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Callable[P, T]:
        info = ''
        if isinstance(args[0], types.Message):
            info = args[0].text
        if isinstance(args[0], types.CallbackQuery):
            info = args[0].data
        try:
            result = func(*args, **kwargs)
            logger.info(f"Function [{func.__name__}] event. Result: {info}")

            return result
        except Exception as error:

            logger.error(
                f"[{error.__class__.__name__}] Function [{func.__name__}] event. Enter value: {error}.")

    return wrapper
