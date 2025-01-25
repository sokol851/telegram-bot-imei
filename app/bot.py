import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from decouple import config
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .database import AsyncSessionLocal
from .models import WhitelistedUser
from .services import flow_get_info, format_response, is_valid_imei

BOT_TOKEN = config('TELEGRAM_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def get_whitelisted_list(db: AsyncSession):
    """ Получение списка пользователей """
    result = await db.execute(select(WhitelistedUser.telegram_id))
    return result.scalars().all()


@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    """ Приветствие при старте бота """
    async with AsyncSessionLocal() as db:
        withe_list = await get_whitelisted_list(db)
    if message.from_user.id in withe_list:
        await message.answer("Добро пожаловать!"
                             " Отправьте мне IMEI вашего"
                             " устройства для проверки.")
    else:
        await message.answer("Извините, у вас нет доступа к этому боту.\nЗарегистрируйтесь командой: '/reg'")


@dp.message(Command(commands=['reg']))
async def register_user(message: types.Message):
    """ Регистрирует пользователя, отправляя POST-запрос к API """
    user_id = message.from_user.id
    payload = {"telegram_id": user_id}

    api_url = 'http://127.0.0.1:8000/api/whitelist/'

    # Запрос на регистрацию
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(api_url, json=payload, timeout=10.0)
        except httpx.RequestError:
            await message.answer("Произошла ошибка при подключении к серверу."
                                 " Пожалуйста, попробуйте позже.")
            return

    # Проверка статусов
    if response.status_code == 201:
        data = response.json()
        token = data.get("token")
        if token:
            await message.answer(f"Вы успешно зарегистрированы!"
                                 f" Ваш токен: `{token}`",
                                 parse_mode="Markdown")
        else:
            await message.answer("Регистрация прошла успешно,"
                                 " но не удалось получить ваш токен.")
    elif response.status_code == 400:
        error_detail = response.json().get('detail', 'Неизвестная ошибка.')
        await message.answer(f"Не удалось зарегистрировать: {error_detail}")
    else:
        await message.answer("Произошла непредвиденная ошибка при регистрации."
                             " Пожалуйста, попробуйте позже.")


@dp.message()
async def handle_imei(message: types.Message):
    """ Запрос на проверку IMEI """
    async with AsyncSessionLocal() as db:
        withe_list = await get_whitelisted_list(db)
    if message.from_user.id not in withe_list:
        await message.answer("Извините, у вас нет доступа к этому боту.\nЗарегистрируйтесь командой: '/reg'")
        return

    imei = message.text.strip()
    if not is_valid_imei(imei):
        await message.answer("Некорректный IMEI. Пожалуйста,"
                             " проверьте и отправьте снова.")
        return

    await message.answer("Проверяю IMEI, пожалуйста подождите...")

    check = await flow_get_info(imei)
    await message.answer(format_response(check['properties']))


async def start_bot():
    await dp.start_polling(bot)
