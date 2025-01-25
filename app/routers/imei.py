from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .. import schemas, services
from ..database import get_db
from ..models import WhitelistedUser

router = APIRouter()


@router.post("/check-imei/",
             summary="Запрос на проверку IMEI",
             response_model=Dict[str, Any],
             status_code=status.HTTP_200_OK)
async def check_imei(imei: schemas.IMEICheckCreate,
                     db: AsyncSession = Depends(get_db)):
    """ Проверка IMEI """
    # Проверка токена в базе данных
    query = select(WhitelistedUser).where(WhitelistedUser.token == imei.token)
    result = await db.execute(query)
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав доступа"
        )

    # Валидация IMEI
    if not services.is_valid_imei(imei.imei):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Некорректный IMEI"
        )

    # Проверка IMEI через сервис
    check = await services.flow_get_info(imei.imei)

    return check
