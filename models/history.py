from datetime import datetime

from sqlalchemy import Column, Integer, JSON, DateTime
from sqlalchemy.sql.schema import ForeignKey

from .database import BaseModel


class History(BaseModel):

    __tablename__ = 'history'

    id_history = Column(Integer, primary_key=True,
                        unique=True, autoincrement=True)
    time_request = Column(DateTime, default=datetime.utcnow(), nullable=False)
    request = Column(JSON, default={}, nullable=False)
    result = Column(JSON, default={})
    id_user = Column(Integer, ForeignKey('users.id_user'))
    
    def __repr__(self):
        return f"<History(id_history='{self.id_history}',\nrequest='{self.request}', result='{self.result}')>"