from datetime import datetime

from sqlalchemy import Column, Integer, JSON, DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.future import select

from .database import BaseModel, async_session

class History(BaseModel):

    __tablename__ = 'history'

    id_history = Column(Integer, primary_key=True,
                        unique=True, autoincrement=True)
    time_request = Column(DateTime, default=datetime.utcnow(), nullable=False)
    request = Column(JSON, default={}, nullable=False)
    result = Column(JSON, default={})
    id_user = Column(Integer, ForeignKey('users.id_user'))

    async def commit(self):
        async with async_session() as session:
            session.add(self)
            await session.commit()
            
    def __repr__(self) -> str:
        return f"{self.id_history}"
