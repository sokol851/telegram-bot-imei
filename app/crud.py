from sqlalchemy import delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import WhitelistedUser
from .schemas import WhitelistedUserCreate


async def get_whitelisted_users(db: AsyncSession,
                                skip: int = 0,
                                limit: int = 100):
    """ Получить всех белых списков """
    result = await db.execute(
        select(WhitelistedUser).offset(skip).limit(limit))
    return result.scalars().all()


async def get_whitelisted_user_by_telegram_id(db: AsyncSession,
                                              telegram_id: int):
    """ Получить пользователя по telegram_id """
    result = await db.execute(select(
        WhitelistedUser).where(WhitelistedUser.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def get_whitelisted_user_by_token(db: AsyncSession, token: str):
    """ Получить пользователя по токену """
    result = await db.execute(select(
        WhitelistedUser).where(WhitelistedUser.token == token))
    return result.scalar_one_or_none()


async def create_whitelisted_user(db: AsyncSession,
                                  user: WhitelistedUserCreate):
    """ Создать нового пользователя """
    db_user = WhitelistedUser(telegram_id=user.telegram_id)
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
    except IntegrityError:
        await db.rollback()
        return None
    return db_user


async def update_whitelisted_user_token(db: AsyncSession,
                                        telegram_id: int,
                                        new_token: str):
    """ Обновить токен пользователя """
    stmt = (
        update(WhitelistedUser)
        .where(WhitelistedUser.telegram_id == telegram_id)
        .values(token=new_token)
        .returning(WhitelistedUser)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()


async def delete_whitelisted_user(db: AsyncSession, telegram_id: int):
    """ Удалить пользователя из белого списка """
    stmt = delete(WhitelistedUser).where(
        WhitelistedUser.telegram_id == telegram_id).returning(WhitelistedUser)
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()
