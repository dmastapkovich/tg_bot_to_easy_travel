import gettext

from loguru import logger

from config import LOCALES_DIR

def setup():
    logger.info(f"Setup locales dir: {LOCALES_DIR}")
    pass