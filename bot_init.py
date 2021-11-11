from aiogram import Bot, Dispatcher
from aiogram.utils.executor import Executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from loguru import logger

import config
from utils.botlogging import setup as logging_setup
from utils.botl_i18n import setup as i18n_setup


bot = Bot(config.TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
execut = Executor(dp)


async def startup(dispatcher: Dispatcher):
    logger.info("Setup Executor aiogram: {url}", url=config.WEBHOOK_URL)
    await dispatcher.bot.set_webhook(config.WEBHOOK_URL)
    
async def shutdown(dispatcher: Dispatcher):
    logger.warning('Shutting down..')

    await dispatcher.bot.delete_webhook()
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


def setup():
    logging_setup()
    logger.info("Setup basic settings")
    i18n_setup()
    execut.on_startup(startup, webhook=True, polling=False)
    execut.on_shutdown(shutdown)
    logger.info("Setup handlers bot_TooEasyTravel")
    import botrequests


def run():
    setup()
    execut.start_webhook(webhook_path=config.WEBHOOK_PATH,
                         host=config.WEBAPP_HOST,
                         port=config.WEBAPP_PORT)
