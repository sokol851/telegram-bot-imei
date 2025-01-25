from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/whitelist")


@router.get("/",
            response_model=List[schemas.WhitelistedUserResponse],
            summary="Белый лист телеграм пользователей")
async def read_whitelisted_users(skip: int = 0,
                                 limit: int = 100,
                                 db: AsyncSession = Depends(get_db)):
    users = await crud.get_whitelisted_users(db, skip=skip, limit=limit)
    return users


@router.get("/{telegram_id}",
            response_model=schemas.WhitelistedUserResponse,
            summary="Получение пользователя")
async def read_whitelisted_user(telegram_id: int,
                                db: AsyncSession = Depends(get_db)):
    user = await crud.get_whitelisted_user_by_telegram_id(
        db, telegram_id=telegram_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@router.post("/",
             response_model=schemas.WhitelistedUserResponseCreate,
             status_code=status.HTTP_201_CREATED,
             summary="Создать пользователя")
async def create_user(user: schemas.WhitelistedUserCreate,
                      db: AsyncSession = Depends(get_db)):
    db_user = await crud.create_whitelisted_user(db, user)
    if db_user is None:
        raise HTTPException(status_code=400,
                            detail="Такой Telegram ID уже существует!")
    return db_user


@router.delete("/{telegram_id}",
               response_model=schemas.WhitelistedUserResponse,
               summary="Удалить пользователя")
async def delete_user(telegram_id: int, db: AsyncSession = Depends(get_db)):
    deleted_user = await crud.delete_whitelisted_user(db,
                                                      telegram_id=telegram_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return deleted_user
