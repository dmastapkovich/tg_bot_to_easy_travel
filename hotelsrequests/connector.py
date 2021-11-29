import aiohttp

from loguru import logger

from config import HEADERS_REQUESTS


@logger.catch
async def get_requests(URL: str, params: dict[str, str | int]) -> dict[str, str | int]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=URL, params=params, headers=HEADERS_REQUESTS) as respons:
            if respons.status == 200:
                logger.info(f"Respons [{URL}] status code: {respons.status}")
                return await respons.json()
            else:
                logger.error(f"[ClientConnectorError] Status code: {respons.status}")
