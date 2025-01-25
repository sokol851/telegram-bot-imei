from sqlalchemy import BigInteger, Column, DateTime, String
from sqlalchemy.sql import func

from .database import Base
from .utils import generate_token


class WhitelistedUser(Base):
    """ Модель белого списка """
    __tablename__ = 'whitelisted_users'

    telegram_id = Column(BigInteger,
                         primary_key=True,
                         index=True)
    token = Column(String(36),
                   unique=True,
                   nullable=False,
                   default=generate_token)
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now())

    def __repr__(self):
        return f"{str(self.telegram_id)}"
