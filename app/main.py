import asyncio

from fastapi import FastAPI

from .bot import start_bot
from .database import Base, engine
from .routers import imei, whitelist

app = FastAPI()

# Подключение маршрутов
app.include_router(imei.router, prefix="/api", tags=["IMEI"])
app.include_router(whitelist.router, prefix="/api", tags=["Users"])


# Создание таблиц при старте
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Запуск бота Telegram в фоновом задании
    asyncio.create_task(start_bot())
