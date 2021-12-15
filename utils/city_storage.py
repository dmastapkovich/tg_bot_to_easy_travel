import json

from aioredis import Redis
from loguru import logger

import config


city_storage = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_CITY_STORAGE,
    decode_responses=True, 
)


@logger.catch
async def get_city_request(input_city: str) -> dict[int, str]:
    result = await city_storage.get(input_city)
    if result:
        return json.loads(result)


@logger.catch
async def set_city(input_city: str, cities: dict):
    await city_storage.set(
        input_city, 
        json.dumps(cities)
    )
