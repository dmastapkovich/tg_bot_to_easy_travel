from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session
from aiogram.types import Message


from config import DATABASE_URL


Base = declarative_base()
engine = create_engine(DATABASE_URL)
session = Session(bind=engine)

COUNTRY_CURR = {
    'en': 'USD',
    'ru': 'RUB'
}

LOCALES = [
    'en', 'ru'
]


class User(Base):

    __tablename__ = 'users'

    id_user = Column(Integer, primary_key=True)
    username = Column(String)
    fullname = Column(String)
    i18n_code = Column(String)
    currency = Column(String)
    route = Column(String)
    request: Column(String)
    # _history: list = None
    dialog: dict['str', str | int] = {}

    __ROUTING = ('ENTER_CITY', 'ENTER_PRICE', 'ENTER_RADIUS', 'ENTER_COUNT_HOTEL',
                 'SELECT_PHOTO', 'ENTER_COUNT_PHOTO', 'CHECK_REQUEST')

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
    def bot_request(self):
        return self.request

    @bot_request.setter
    def bot_request(self, value):
        if value not in self.__REQUESTS:
            value = ''
        self.request = value
        User.commit_user(self)

    @staticmethod
    def from_message(messge: Message):
        user = User(
            username=messge.from_user.username,
            fullname=messge.from_user.full_name,
            id_user=messge.from_user.id,
            i18n_code=messge.from_user.language_code,
            currency=COUNTRY_CURR[messge.from_user.language_code],
            route=''
        )

        result = User.user_from_db(user)

        if len(result) == 0:
            User.commit_user(user)
        else:
            user = result[0]

        return user

    @staticmethod
    def user_from_db(user) -> list:
        return session.query(User).filter(User.id_user == user.id_user).all()

    @staticmethod
    def commit_user(user):
        session.add(user)
        session.commit()

    def __repr__(self):
        return "<User(chat_id='%s', fullname='%s', username='%s')>" % (
            self.id_user, self.fullname, self.username)
