from aiogram.dispatcher.filters.state import State, StatesGroup


class StateBot(StatesGroup):
    ENTER_CITY = State()
    SELECT_CITY = State()
    ENTER_PRICE = State()
    ENTER_RADIUS = State()
    ENTER_COUNT_HOTEL = State()
    SELECT_PHOTO = State()
    ENTER_COUNT_PHOTO = State()
    CHECK_REQUEST = State()
    SETTINGS_OPTION_MENU = State()
    COMMIT_SETTINGS = State()
