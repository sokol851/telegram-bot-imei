import httpx
from decouple import config
from fastapi import HTTPException

# Переключение токенов с тестового на живой
# IMEICHECK_TOKEN = config('IMEICHECK_LIVE_TOKEN')
IMEICHECK_TOKEN = config('IMEICHECK_SANDBOX_TOKEN')


async def flow_get_info(imei):
    """ Создание заказа """
    url = "https://api.imeicheck.net/v1/checks"

    payload = {
        "deviceId": str(imei),
        "serviceId": 12
    }
    headers = {
        'Authorization': f'Bearer {IMEICHECK_TOKEN}',
        'Accept-Language': 'en',
        'Content-Type': 'application/json'
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Ошибка HTTP: {e.response.text}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Произошла ошибка: {str(e)}"
            )


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

    message = "📱 Информация о IMEI\n\n"

    # Обработка основных свойств
    for key, label in data.items():
        message += f"{key}: {label}\n"
    return message
