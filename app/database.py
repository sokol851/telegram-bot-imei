from decouple import config
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = config('DATABASE_URL',
                      default='sqlite+aiosqlite:///./db.sqlite3')

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


# Зависимость для получения сессии БД
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
