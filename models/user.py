from aiogram.types import Message
from sqlalchemy import Column, Integer, String
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from config import LOCALES, COUNTRY_CURR, SETTINGS_CURR, SETTINGS_LOCALES
from .database import BaseModel, async_session
from .history import History


class User(BaseModel):
    __tablename__ = 'users'

    id_user = Column(Integer, primary_key=True, index=True, unique=True)
    locale = Column(String)
    currency = Column(String)
    _history = relationship("History", uselist=False)

    async def get_history(self) -> list:
        async with async_session() as session:
            result = await session.execute(
                select(History).where(History.id_user == self.id_user)
            )
        return result.scalars().all()

    async def set_history(self, request: dict[str, str | int], result: dict[str, str | int]):
        await History(id_user=self.id_user,
                      request=request,
                      result=result).commit()

    async def set_settings(self, option, value):
        if option == 'locale':
            self.locale = value
        else:
            self.currency = value
        await self.commit()

    async def get_settings(self):
        return '\n'.join([
            "Ваши текущие настройки:",
            f"Язык отображения сообщений: *{SETTINGS_LOCALES.get(self.locale)}*",
            f"Используемая валюта: *{SETTINGS_CURR.get(self.currency)}*",
            "Выберите опцию настройки:"
        ])

    async def commit(self):
        async with async_session() as session:
            session.add(self)
            await session.commit()
        return self

    @classmethod
    async def from_message(cls, messge: Message):
        _locale = LOCALES.get(messge.from_user.language_code, 'ru_RU')
        _currency = COUNTRY_CURR.get(messge.from_user.language_code, 'RUB')

        user = User(id_user=messge.from_user.id,
                    locale=_locale,
                    currency=_currency)

        async with async_session() as session:
            result = await session.execute(
                select(User).where(User.id_user == user.id_user)
            )
            userdb = result.scalars().first()

        cls = await user.commit() if not userdb else userdb
        return cls
