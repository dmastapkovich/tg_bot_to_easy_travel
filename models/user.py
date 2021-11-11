from aiogram.types import Message

COUNTRY_CURR = {
    'en': 'USD',
    'ru': 'RUB'
}

LOCALES = [
    'en', 'ru'
]


class User:

    _history: list = None
    _next_hop: str = None
    _bot_request: str = None
    _dialog: dict['str', str | int] = {}
    __ROUTING = ('ENTER_CITY', 'ENTER_PRICE', 'ENTER_RADIUS', 'ENTER_COUNT_HOTEL',
                 'SELECT_PHOTO', 'ENTER_COUNT_PHOTO', 'CHECK_REQUEST')
    __BOT_REQUESTS = ('lowprice', 'highprice', 'bestdeal')

    def __init__(self, username: str, fullname: str, chat_id: int, language_code: str) -> None:
        self._username = username
        self._fullname = fullname
        self._user_id = chat_id

        # Settings user
        self._language = language_code
        self._currency = COUNTRY_CURR[self.language] if COUNTRY_CURR.get(
            self.language) else COUNTRY_CURR['en']

    @property
    def history(self) -> list:
        return self._history

    @property
    def language(self):
        return self.language

    @language.setter
    def set_language(self, value):
        if value not in LOCALES:
            value = 'en'
        self.language = value

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def set_currency(self, value):
        if not COUNTRY_CURR.get(value):
            value = COUNTRY_CURR['en']
        self.language = value

    def change_settings(self, language_code, currency_code):
        self.language = language_code
        self.currency = currency_code

    @property
    def next_hop(self):
        return self._next_hop

    @next_hop.setter
    def set_next_hop(self, route):
        if route not in self.__ROUTING:
            route = None
        self._next_hop = route

    @property
    def bot_request(self):
        return self._bot_request

    @bot_request.setter
    def set_bot_request(self, value):
        if value not in self.__BOT_REQUESTS:
            value = None
        self._bot_request = value

    @staticmethod
    def from_message(messge: Message):
        return User(
            username=messge.from_user.username,
            fullname=messge.from_user.full_name,
            chat_id=messge.from_user.id,
            l18n_code=messge.from_user.language_code
        )
