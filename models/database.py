import os

import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session
from loguru import logger

from config import DATABASE_URL_DRIVER, DATABASE_URL_FILE


Base = declarative_base()
session = Session()

class BaseModel(Base):
    __abstract__ = True


def setup():
    logger.info("Setup DataBase Connection sqlite")
    
    from .history import History
    from .user import User
    
    engine = create_engine(DATABASE_URL_DRIVER)
    session.bind = engine
    try:
        if not os.path.isfile(DATABASE_URL_FILE):
            raise sqlite3.DatabaseError(
                f'No such database: {DATABASE_URL_FILE}')
    except sqlite3.DatabaseError as error:
        logger.error(f"[DATABASE] {error}")
        BaseModel.metadata.create_all(engine)
        logger.info(f"[DATABASE] Database created {DATABASE_URL_FILE}")
