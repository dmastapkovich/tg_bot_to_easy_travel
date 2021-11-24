from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.orm import relationship
from aiogram.types import Message

from .database import BaseModel, session
from .history import History

COUNTRY_CURR: dict = {
    'en': 'USD',
    'ru': 'RUB'
}

LOCALES: dict = {
    'en': 'en_US',
    'ru': 'ru_RU'
}


class User(BaseModel):

    __tablename__ = 'users'

    id_user = Column(Integer, primary_key=True, index=True, unique=True)
    username = Column(String, unique=True)
    fullname = Column(String)
    locale = Column(String, default='ru')
    currency = Column(String, default='RUB')
    route = Column(String, default='', nullable=False)
    request = Column(String, default='', nullable=False)
    dialog = Column(JSON, default={}, nullable=False)
    history = relationship("History", uselist=False)

    __ROUTING = ('ENTER_CITY', 'SELECT_CITY', 'ENTER_PRICE', 'ENTER_RADIUS',
                 'ENTER_COUNT_HOTEL', 'SELECT_PHOTO', 'ENTER_COUNT_PHOTO', 'CHECK_REQUEST')

    __REQUESTS = ('/lowprice', '/highprice', '/bestdeal')

    @property
    def next_hop(self):
        return self.route

    @next_hop.setter
    def next_hop(self, value):
        if value not in self.__ROUTING:
            value = ''
        self.route = value
        User.commit_user(self)

    @property
    def bot_request(self) -> str:
        return self.request

    @bot_request.setter
    def bot_request(self, value: str):
        if value not in self.__REQUESTS:
            value = ''
        self.request = value
        self.dialog = {
            'locale': self.locale,
            'currency': self.currency
        }
        User.commit_user(self)

    def set_item_dialog(self, key: str, value: str | int):
        self.dialog[key] = value
        flag_modified(self, 'dialog')
        User.commit_user(self)

    def set_history_request(self, result):
        history = History(
            request=self.dialog,
            result=result,
            id_user=self.id_user
        )
        User.commit_history(history)

    def get_history(self) -> list:
        return session.query(History).filter(History.id_user == self.id_user).all()

    @classmethod
    def from_message(cls, messge: Message):

        user = User(
            username=messge.from_user.username,
            fullname=messge.from_user.full_name,
            id_user=messge.from_user.id,

            locale=LOCALES[messge.from_user.language_code]
            if LOCALES.get(messge.from_user.language_code)
            else 'ru_RU',

            currency=COUNTRY_CURR[messge.from_user.language_code]
            if COUNTRY_CURR.get(messge.from_user.language_code)
            else 'RUB'
        )

        result = User.user_from_db(user)

        if len(result) == 0:
            User.commit_user(user)
            cls = user
        else:
            cls = result[0]

        return cls

    @staticmethod
    def user_from_db(user) -> list:
        return session.query(User).filter(User.id_user == user.id_user).all()

    @staticmethod
    def commit_user(user):
        session.add(user)
        session.commit()

    @staticmethod
    def commit_history(history):
        session.add(history)
        session.commit()

    def __repr__(self):
        return "<User(chat_id='%s', fullname='%s', username='%s')>" % (
            self.id_user, self.fullname, self.username)
