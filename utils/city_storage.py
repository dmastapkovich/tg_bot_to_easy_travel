from typing import Any
from aioredis import Redis
from loguru import logger

import config


city_storage = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_CITY_STORAGE,
    decode_responses=True
)


@logger.catch
async def get_city_request(input_city: str) -> dict[int, str]:
    return await city_storage.hgetall(input_city)


@logger.catch
async def set_city(input_city: str, cities: dict):
    return await city_storage.hmset(input_city, cities)
