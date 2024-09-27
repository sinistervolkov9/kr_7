import requests
from config import settings


def send_telegram_message(chat_id, message):
    params = {
            'text': message,
            'chat_id': chat_id
        }

    url = f'{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage'
    response = requests.get(url, params=params, timeout=10)
    if not response.ok:
        raise RuntimeError("Failed to sent telegram message")
