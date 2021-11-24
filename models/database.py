import os

from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from loguru import logger

from config import DATABASE_URL_DRIVER, DATABASE_URL_FILE


Base = declarative_base()
async_session = sessionmaker(expire_on_commit=False,
                             class_=AsyncSession)


class BaseModel(Base):
    __abstract__ = True


async def setup_db(dispatcher: Dispatcher):
    from .history import History
    from .user import User

    engine = create_async_engine(DATABASE_URL_DRIVER)

    if not os.path.isfile(DATABASE_URL_FILE):
        logger.warning(f"[DATABASE] No such database: {DATABASE_URL_FILE}")

        async with engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)

        logger.warning(f"[DATABASE] Database created {DATABASE_URL_FILE}")

    async_session.configure(bind=engine)
    logger.info(f"DataBase {DATABASE_URL_DRIVER} connected")
