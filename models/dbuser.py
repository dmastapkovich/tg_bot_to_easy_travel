from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session
from aiogram import Dispatcher
from aiogram.utils.executor import Executor
from loguru import logger

from ..config import DATABASE_URL


Base = declarative_base()
engine = create_engine(DATABASE_URL)
session = Session(bind=engine)


class UserDB(Base):

    __tablename__ = 'users'

    id_user = Column(Integer, primary_key=True)
    username = Column(String)
    fullname = Column(String)
    i18n_code = Column(String)
    currency = Column(String)
    route = Column(String)

    def __repr__(self):
        return "<User(id='%s', fullname='%s', username='%s')>" % (
            self.id_user, self.fullname, self.username)
