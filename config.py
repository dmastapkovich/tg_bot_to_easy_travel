from os import getcwd, path

from loguru import logger

from envparse import env, ConfigurationError


try:
    # i18n storage
    BOT_DIR: str = getcwd()
    LOCALES_DIR = path.join(BOT_DIR, 'locales')
    LOGGER_FILE = path.join(BOT_DIR, 'logs', 'log_file.log')

    # TOKEN Telegram bot
    TELEGRAN_TOKEN: str = env.str("TELEGRAN_TOKEN", default='2088846652:AAHZ73ULPkpC3d207mJ-wbTtAQUY6-stK-c')

    # webhook settings
    WEBHOOK_DOMAIN = env.str(
        "WEBHOOK_DOMAIN", default='a2e8-188-128-56-107.ngrok.io')
    WEBHOOK_PATH = ''
    WEBHOOK_URL = f"https://{WEBHOOK_DOMAIN}{WEBHOOK_PATH}"

    # webserver settings
    WEBAPP_HOST = env.str("WEBAPP_HOST", default="localhost")
    WEBAPP_PORT = env.str("WEBAPP_PORT", default="8080")

    # DataBase settings
    DATABASE_NAME = env.str("DATABASE_NAME", default='traveldb.db')
    DATABASE_URL_DRIVER = f"sqlite+aiosqlite:///{DATABASE_NAME}"
    DATABASE_URL_FILE = path.join(BOT_DIR, DATABASE_NAME)

    # Redis default settings
    REDIS_HOST = env.str("REDIS_HOST", default='localhost')
    REDIS_PORT = env.str("REDIS_PORT", default=6379)
    REDIS_NUMBER_DB = env.str("REDIS_NUMBER_DB", default=1)
    REDIS_POOL_SIZE = env.str("REDIS_POOL_SIZE", default=10)

    # Hotels API
    HOTELS_URL = 'hotels4.p.rapidapi.com'
    HOTELS_TOKEN = env.str("HOTELS_TOKEN", default='123')

    HEADERS_REQUESTS = {
        'x-rapidapi-host': HOTELS_URL,
        'x-rapidapi-key': HOTELS_TOKEN
    }

    SERCH_LOCATION_URL = 'https://hotels4.p.rapidapi.com/locations/v2/search'
    SERCH_HOTEL_URL = 'https://hotels4.p.rapidapi.com/properties/list'
    SERCH_PHOTO_HOTEL_URL = 'https://hotels4.p.rapidapi.com/properties/get-hotel-photos'
    HOTEL_URL_FORMAT = "https://hotels.com/ho{hotel_id}"

    # CONSTANTS
    SZ_COUNT_HOTEL = 5
    SZ_COUNT_PHOTO = 5
    SZ_RADIUS = 5

except ConfigurationError as error:
    logger.exception(f"[{error.__class__.__name__}] {error}")
    raise SystemExit(error)

COUNTRY_CURR: dict = {
    'en': 'USD',
    'ru': 'RUB'
}

LOCALES: dict = {
    'en': 'en_US',
    'ru': 'ru_RU'
}

SETTINGS_CURR: dict = {
    'USD': '$',
    'EUR': '€',
    'RUB': '₽'
}

SETTINGS_LOCALES: dict = {
    'en_US': 'English',
    'ru_RU': 'Русский'
}

INFO_COMMAND = '\n'.join([
    "List of commands for bot:",
    "/start - Start bot",
    "/help - Info about bot and its command",
    "/lowprice - Search for low price hotels",
    "/highprice - Search for high price hotels",
    "/bestdeal - Search hotels by parameters",
    "/history - Output history",
    "/settings - User Settings"
])
