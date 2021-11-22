from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from aiogram import Bot, Dispatcher
from aiogram.dispatcher import storage
from aiogram.utils.executor import Executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from loguru import logger

import config
import utils.botlogging as logging
import utils.botl_i18n as i18n
import models.database as database


storage = MemoryStorage()
# storage = RedisStorage2(
#     host=config.REDIS_HOST,
#     port=config.REDIS_PORT,
#     db=config.REDIS_NUMBER_DB,
#     pool_size=config.REDIS_POOL_SIZE,
#     prefix='FSM_REDIS_STORAGE'
# )

bot = Bot(config.TELEGRAN_TOKEN)

dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

execut = Executor(dp)


async def startup(dispatcher: Dispatcher):
    logger.info("Setup Executor aiogram: {url}", url=config.WEBHOOK_URL)
    await dispatcher.bot.set_webhook(config.WEBHOOK_URL)
    
async def shutdown(dispatcher: Dispatcher):
    logger.warning('Shutting down..')

    await dispatcher.bot.delete_webhook()


def setup():
    logging.setup()
    logger.info("Setup basic settings")
    i18n.setup()
    execut.on_startup([startup, database.setup_db], webhook=True, polling=False)
    execut.on_shutdown(shutdown)
    logger.info("Setup handlers bot_TooEasyTravel")
    import botrequests


def run():
    setup()
    execut.start_webhook(webhook_path=config.WEBHOOK_PATH,
                         host=config.WEBAPP_HOST,
                         port=config.WEBAPP_PORT)
