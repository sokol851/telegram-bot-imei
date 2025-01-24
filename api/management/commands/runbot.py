import asyncio
import logging

from django.core.management.base import BaseCommand

from api.bot import main

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Запуск Telegram-бота'

    def handle(self, *args, **options):
        try:
            logger.info("Запуск Telegram-бота...")
            asyncio.run(main())
        except KeyboardInterrupt:
            logger.info("Остановка Telegram-бота (KeyboardInterrupt)")
        except Exception as e:
            logger.error(f"Ошибка при запуске бота: {e}")
