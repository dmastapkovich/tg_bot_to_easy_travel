import asyncio
import aiohttp

from loguru import logger

from config import HEADERS_REQUESTS


@logger.catch
async def get_requests(URL: str, params: dict[str, str | int], recursion=0) -> dict[str, str | int]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=URL, params=params, headers=HEADERS_REQUESTS) as respons:
            if respons.status == 200:
                logger.info(f"Respons [{URL}] status code: {respons.status}")
                return await respons.json()
            if respons.status == 429 and recursion < 5:
                logger.error(f"[Throttling] Status code: {respons.status}. URL: {URL}")
                await asyncio.sleep(1)
                return await get_requests(URL, params, recursion+1)
            if respons.status == 429 and recursion == 5:
                logger.error(f"[APIHOTELS ERROR] Status code: {respons.status}")
            else:
                logger.error(f"[ClientConnectorError] Status code: {respons.status}")
