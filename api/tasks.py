# api/tasks.py

import requests
from celery import shared_task
from django.conf import settings


@shared_task
def check_imei_task(imei):
    """ Валидация IMEI """
    if not is_valid_imei(imei):
        return {'error': 'Неверный формат IMEI'}

    params = {
        'token': settings.IMEICHECK_SANDBOX_TOKEN,
        'imei': imei
    }

    try:
        response = requests.get(settings.IMEICHECK_API_URL, params=params)
        data = response.json()
        return data
    except Exception as e:
        return {'error': str(e)}


def is_valid_imei(imei):
    """ Валидация IMEI """

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
