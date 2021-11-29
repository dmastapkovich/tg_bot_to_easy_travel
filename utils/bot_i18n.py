
from typing import Tuple, Any

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aioredis import Redis

import config
from models import User
from loguru import logger


locale_storage = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_LOCALES_STORAGE,
    decode_responses=True
)


class Localization(I18nMiddleware):
    @logger.catch
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        _body: types.User = types.User.get_current()
        user_id = _body.id
    
        if not await locale_storage.get(user_id):
            user: User = await User.from_user(_body)
            await locale_storage.set(user_id, user.i18n_code)

        return await locale_storage.get(user_id)
