import aiogram
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.executor import Executor

from loguru import logger

import config
from models.database import db_setup
from utils import logging_setup, redis_setup
from utils.bot_i18n import Localization

try:
    fsm_storage = RedisStorage2(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.REDIS_FSM_STORAGE,
        pool_size=config.REDIS_POOL_SIZE,
        prefix='FSM_REDIS_STORAGE'
    )

    bot = Bot(config.TELEGRAM_TOKEN)
    dp = Dispatcher(bot, storage=fsm_storage)
    execut = Executor(dp)

    i18n = Localization(config.I18N_DOMAIN, config.LOCALES_DIR)

except (aiogram.exceptions.BadRequest, RuntimeError) as error:
    logger.exception(f"[{error.__class__.__name__}] {error}")
    raise SystemExit(f"[{error.__class__.__name__} -> {__name__}] {error}")


def _(text: str):
    try:
        return str(i18n.lazy_gettext(text))
    except Exception as error:
        logger.exception(f"[{error.__class__.__name__}] {error}")
        return '[ERROR] Error accessing bot'


async def middleware_setup(dispatcher: Dispatcher):
    logger.info(
        f"Setup internationalize middleware. DOMAIN: {config.I18N_DOMAIN}")
    dispatcher.middleware.setup(i18n)

    logger.info("Setup logging middleware.")
    dispatcher.middleware.setup(LoggingMiddleware())


async def start_bot(dispatcher: Dispatcher):
    logger.info("Import handlers bot_TooEasyTravel")
    import botrequests

    logger.info("Setup Executor aiogram: {url}", url=config.WEBHOOK_URL)
    await dispatcher.bot.set_webhook(config.WEBHOOK_URL)


async def shutdown(dispatcher: Dispatcher):
    logger.warning('Shutting down..')
    await dispatcher.bot.delete_webhook()


def setup():
    logger.info("Setup basic settings")
    execut.on_startup([logging_setup, db_setup, middleware_setup, redis_setup, start_bot],
                      webhook=True, polling=False)
    execut.on_shutdown(shutdown)


@logger.catch
def run():
    try:
        setup()
        execut.start_webhook(webhook_path=config.WEBHOOK_PATH,
                             host=config.WEBAPP_HOST,
                             port=config.WEBAPP_PORT)
    except SystemExit as error:
        logger.exception(error)
