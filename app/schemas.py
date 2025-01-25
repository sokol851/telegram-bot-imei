from datetime import datetime

from pydantic import BaseModel, Field


class IMEICheck(BaseModel):
    """ Базовая схема проверки IMEI """
    imei: str = Field(max_length=15)

    class Config:
        from_attributes = True


class IMEICheckCreate(IMEICheck):
    """ Схема проверки IMEI при создании """
    imei: str = Field(max_length=15)
    token: str = Field(max_length=50)

    class Config:
        from_attributes = True


class WhitelistedUserBase(BaseModel):
    """ Базовая схема белого списка """
    telegram_id: int


class WhitelistedUserCreate(WhitelistedUserBase):
    """ Схема создания пользователя """
    pass


class WhitelistedUserResponseCreate(WhitelistedUserBase):
    """ Схема создания пользователя """
    telegram_id: int
    token: str = Field(min_length=36, max_length=36)


class WhitelistedUserUpdate(BaseModel):
    """ Схема обновления пользователя """
    token: str = Field(min_length=36, max_length=36)


class WhitelistedUserResponse(WhitelistedUserBase):
    """ Схема получения пользователя """
    telegram_id: int
    created_at: datetime

    class Config:
        from_attributes = True
