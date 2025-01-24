import json
import time

import requests

from config import settings


def post_order(imei):
    """ Создание заказа """
    url = "https://api.imeicheck.net/v1/orders"

    payload = json.dumps({
        "deviceIds": [
            str(imei)
        ],
        "serviceId": 6,
        "duplicateProcessingType": "reprocess"
    })
    headers = {
        'Authorization': f'Bearer {settings.IMEICHECK_LIVE_TOKEN}',
        'Accept-Language': 'en',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def get_status_order(id):
    """ Получение статуса заказа """
    url = f"https://api.imeicheck.net/v1/orders/{id}"

    payload = {}
    headers = {
        'Authorization': f'Bearer {settings.IMEICHECK_LIVE_TOKEN}',
        'Accept-Language': 'en',
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()['status']


def get_check(id):
    """ Получение информации об IMEI """
    url = "https://api.imeicheck.net/v1/checks/xpOkg_EsIZoDzVXZ"

    payload = {}
    headers = {
        'Authorization': f'Bearer {settings.IMEICHECK_LIVE_TOKEN}',
        'Accept-Language': 'en',
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def flow_get_info(imei):
    """ Флоу работы с сервисом """

    # Создаём заказ
    order = post_order(imei)

    # Проверяем статус заказа каждые 5 сек
    status = get_status_order(order['id'])
    while status == 'processing':
        time.sleep(5)
        status = get_status_order(order['id'])
        if status == 'successful':
            # Если выполнен - получаем информацию
            check = get_check(order['checks'][0]['id'])
            return check
        if status == 'failure':
            failure = {'failure': 'Ошибка запроса'}
            return failure
