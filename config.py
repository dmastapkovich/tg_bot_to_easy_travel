from os import getcwd, path

from envparse import env

BOT_DIR: str = getcwd()
LOCALES_DIR = path.join(BOT_DIR, 'locales')
LOGGER_FILE = path.join(BOT_DIR, 'logs', 'log_file.log')

# TOKEN Telegram bot
TELEGRAN_TOKEN: str = env.str("TELEGRAN_TOKEN")

# webhook settings
WEBHOOK_DOMAIN = env.str("WEBHOOK_DOMAIN", default='6327-128-69-190-135.ngrok.io')
WEBHOOK_PATH = ''
WEBHOOK_URL = f"https://{WEBHOOK_DOMAIN}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = env.str("WEBAPP_HOST", default="localhost")
WEBAPP_PORT = env.str("WEBAPP_PORT", default="8080")

DATABASE_NAME = env.str("DATABASE_NAME", default='traveldb.db')
DATABASE_URL_DRIVER = f"sqlite:///{DATABASE_NAME}"
DATABASE_URL_FILE = path.join(BOT_DIR, DATABASE_NAME)

HOTELS_URL = 'hotels4.p.rapidapi.com'
HOTELS_TOKEN = env.str("HOTELS_TOKEN")

HEADERS_REQUESTS = {
    'x-rapidapi-host': HOTELS_URL,
    'x-rapidapi-key': HOTELS_TOKEN
}

SZ_COUNT_HOTEL = 5
SZ_COUNT_PHOTO = 5
SZ_RADIUS = 5