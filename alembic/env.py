import asyncio
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models import Base

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata


def get_url():
    from decouple import config
    return config("DATABASE_URL")


def run_migrations_offline():
    """Запуск миграций в офлайн режиме."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Запуск миграций в онлайн режиме."""
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix='sqlalchemy.',
            poolclass=pool.NullPool,
            url=get_url(),
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
