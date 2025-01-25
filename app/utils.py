import uuid


def generate_token() -> str:
    """ Генерирует токен для пользователя """
    return str(uuid.uuid4())
