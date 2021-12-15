from aiogram import types
from sqlalchemy import Column, Integer, String
from sqlalchemy.future import select
from sqlalchemy.orm import relationship

from config import LOCALES, COUNTRY_CURR
from .database import BaseModel, async_session
from .history import History


class User(BaseModel):
    __tablename__ = 'users'

    id_user = Column(Integer, primary_key=True, index=True, unique=True)
    locale = Column(String)
    i18n_code = Column(String)
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

    async def set_settings(self, option: str, value: str):
        if option == 'locale':
            self.i18n_code = value.split('_')[0]
            self.locale = value
        else:
            self.currency = value
        await self.commit()

    async def commit(self):
        async with async_session() as session:
            session.add(self)
            await session.commit()
        return self

    @classmethod
    async def from_user(cls, user: types.User):
        _locale = LOCALES.get(user.language_code, 'ru_RU')
        _currency = COUNTRY_CURR.get(user.language_code, 'RUB')
        _i18n_code = 'ru'
        user = User(id_user=user.id,
                    locale=_locale,
                    i18n_code=_i18n_code,
                    currency=_currency)

        async with async_session() as session:
            result = await session.execute(
                select(User).where(User.id_user == user.id_user)
            )
            userdb = result.scalars().first()

        cls = await user.commit() if not userdb else userdb
        return cls

    @classmethod
    async def from_message(cls, messge: types.Message):
        return await User.from_user(messge.from_user)
