from os import getcwd, path


BOT_DIR: str = getcwd()
LOCALES_DIR = path.join(BOT_DIR, 'locales')
LOGGER_FILE = path.join(BOT_DIR, 'log_file.log')

# TOKEN Telegram bot
TOKEN: str = '2088846652:AAHZ73ULPkpC3d207mJ-wbTtAQUY6-stK-c'

# webhook settings
WEBHOOK_HOST = 'https://e5c1-188-128-56-107.ngrok.io'
WEBHOOK_PATH = ''
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 8080

DATABASE_URL = "sqlite:///traveldb.db"
