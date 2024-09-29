import requests
from config.settings import TELEGRAM_TOKEN, TELEGRAM_URL
from .models import Habit


def message_create(habit_id):
    """Создаем сообщение."""

    habit = Habit.objects.get(id=habit_id)

    user = habit.user
    name = name_of_user(user.email)

    time = habit.time
    if habit.place is None:
        place = "Любое место"
    else:
        place = habit.place

    action = habit.action

    if habit.connection_habit_id:
        message = (f"Доброго времени суток {name}! Пришло время({time})! Необходимо выполнить({action}),"
                   f" в условленном месте({place}),"
                   f" а за это можешь: {Habit.objects.get(id=habit.connection_habit_id).action}!")
    elif habit.reward:
        message = (f"Доброго времени суток {name}! Пришло время({time})! Необходимо выполнить({action}),"
                   f" в условленном месте({place}), а за это можешь: {habit.reward}!")
    else:
        message = (f"Доброго времени суток {name}! Пришло время({time})! Необходимо выполнить({action}),"
                   f" в условленном месте({place}).")

    return message


def send_tg(chat_id, message):
    params = {
        "text": message,
        "chat_id": chat_id,
    }
    requests.post(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage", params=params)


def name_of_user(email):
    """Формируем имя из почтового адреса. Берем все, что до @."""
    name = ""
    for letter in email:
        if letter != "@":
            name += letter
        else:
            break
    return name
