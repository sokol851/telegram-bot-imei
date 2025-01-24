import asyncio
import os
from datetime import datetime

import django
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from decouple import config

from api.services import flow_get_info

# Укажите путь к вашему файлу настроек
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Инициализируйте Django
django.setup()

# Теперь можно импортировать модели
from api.models import WhitelistedUser

# Получаем список значений id_telegram
WITHE_LIST = list(WhitelistedUser.objects.values_list('telegram_id', flat=True))

# Токен бота
BOT_TOKEN = config('TELEGRAM_TOKEN')

# Создание бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    """ Приветствие при старте бота """
    if message.from_user.id in WITHE_LIST:
        await message.answer("Добро пожаловать! "
                             "Отправьте мне IMEI вашего устройства "
                             "для проверки.")
    else:
        await message.answer("Извините, у вас нет доступа к этому боту.")


@dp.message()
async def handle_imei(message: types.Message):
    """ Запрос на проверку IMEI """
    if message.from_user.id not in WITHE_LIST:
        await message.answer("Извините, у вас нет доступа к этому боту.")
        return

    imei = message.text.strip()
    if not is_valid_imei(imei):
        await message.answer("Некорректный IMEI. Пожалуйста, "
                             "проверьте и отправьте снова.")
        return

    await message.answer("Проверяю IMEI, пожалуйста подождите...")

    check = flow_get_info(imei)
    if check != {'failure': 'Ошибка запроса'}:
        await message.answer(format_response(check['properties']))
    else:
        await message.answer("Произошла ошибка при проверке IMEI.")


def is_valid_imei(imei):
    """ Валидация IMEI алгоритмом Луна """

    def luhn_checksum(num):
        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(num)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        total = sum(odd_digits)
        for d in even_digits:
            total += sum(digits_of(d * 2))
        return total % 10

    try:
        imei = ''.join(filter(str.isdigit, imei))
        if len(imei) != 15:
            return False
        return luhn_checksum(imei) == 0
    except Exception:
        return False


def format_response(data):
    """ Форматирование ответа для телеграм-бота """
    if 'error' in data:
        return f"Ошибка: {data['error']}"

    imei = data.get('imei', 'N/A')
    imei2 = data.get('imei2', 'N/A')
    device_name = data.get('deviceName', 'N/A')
    model_code = data.get('modelCode', 'N/A')
    serial = data.get('serial', 'N/A')
    unlock_number = data.get('unlockNumber', 'N/A')
    mi_activation_lock = data.get('miActivationLock', 'N/A')
    sku_number = data.get('skuNumber', 'N/A')
    purchase_country = data.get('purchaseCountry', 'N/A')
    warranty_status = data.get('warrantyStatus', 'N/A')

    # Обработка дат
    def format_date(timestamp):
        try:
            return datetime.fromtimestamp(int(timestamp)).strftime("%d.%m.%Y %H:%M:%S")
        except (ValueError, TypeError):
            return 'N/A'

    message = (
        f"📱 Информация о IMEI\n\n"
        f"Название: {device_name}\n"
        f"Модель: {model_code}\n"
        f"IMEI1: {imei}\n"
        f"IMEI2: {imei2}\n"
        f"S/N: {serial}\n"
        f"Номер разблокировки: {unlock_number}\n"
        f"mi активация: {mi_activation_lock}\n"
        f"sku number: {sku_number}\n"
        f"Страна производства: {purchase_country}\n"
        f"Статус гарантии: {warranty_status}\n"
        f"Дата изготовления: {format_date(data.get('productionDate'))}\n"
        f"Дата отправки: {format_date(data.get('deliveryDate'))}\n"
        f"Дата активации: {format_date(data.get('activationDate'))}\n"
    )
    return message


async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
