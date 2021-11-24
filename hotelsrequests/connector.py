import aiohttp

from loguru import logger

from config import HEADERS_REQUESTS


async def get_requests(URL: str, params: dict[str, str | int]) -> dict[str, str | int]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                    url=URL,
                    params=params,
                    headers=HEADERS_REQUESTS
                    ) as respons:
                return await respons.json()

        except aiohttp.ClientError as error:
            logger.error(f"[{error.__class__.__name__}] {error}")
