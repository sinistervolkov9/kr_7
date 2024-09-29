import asyncio
from celery import shared_task
from .models import Habit
from habits.telegram import send_message
from asgiref.sync import async_to_sync
from config.celery import app

@app.task
def send_telegram_notification():
    print("Send")
    habits = Habit.objects.filter(status='active', user__telegram_chat_id__isnull=False)

    for habit in habits:
        user = habit.user
        message = f"Напоминание! Ваша привычка {habit.action} ожидает выполнения!"

        print(user)
        print(message)

        # Выполняем асинхронную функцию синхронно
        async_to_sync(send_message)(user.telegram_chat_id, message)


# @shared_task
# def send_telegram_notification():
#     print("Send")
#     habits = Habit.objects.filter(status='active', user__telegram_chat_id__isnull=False)
#
#     for habit in habits:
#         user = habit.user
#         message = f"Напоминание! Ваша привычка {habit.action} ожидает выполнения!"
#
#         print(user)
#         print(message)
#
#         asyncio.run(send_message(user.telegram_chat_id, message))

# ----------------------------------------------------------------------------------------------------------------------

# from celery import shared_task
# from .models import Habit
# import asyncio
# from habits.telegram import send_message
#
#
# @shared_task
# def send_telegram_notification():
#     print("Начало отправки уведомлений")
#
#     habits = Habit.objects.filter(status='active', user__telegram_chat_id__isnull=False)
#
#     async def send_notifications():
#         tasks = []
#         for habit in habits:
#             user = habit.user
#             message = f"Напоминание! Ваша привычка: {habit.action} ожидает выполнения!"
#
#             print(f"Отправка уведомления пользователю {user.username} ({user.telegram_chat_id}): {message}")
#
#             # Добавляем задачу для отправки сообщения в список
#             tasks.append(send_message(user.telegram_chat_id, message))
#
#         # Выполняем все задачи параллельно
#         await asyncio.gather(*tasks)
#
#     # Запускаем все асинхронные задачи
#     asyncio.run(send_notifications())


# @shared_task
# def telegram_notification():
#     current_time = datetime.datetime.now().replace(second=0, microsecond=0)
#     current_time_plus_5 = current_time + datetime.timedelta(minutes=5)
#
#     habits = Habit.objects.filter(habit_is_pleasant=False)
#
#     for habit in habits:
#         if str(habit.time) == str(current_time_plus_5.strftime("%X")):
#             chat_id = habit.user.chat_id
#             if chat_id:
#                 count = habit.number_of_executions
#                 if count != 0:
#                     text_message = message_create(habit.pk)
#                     send_tg(chat_id=chat_id, message=text_message)
#                     count -= 1
#                     habit.save()

# @shared_task()
# def telegram_notification():
#     zone = pytz.timezone(settings.TIME_ZONE)
#     current_time = datetime.now(zone)
#     current_time_less = current_time - timedelta(minutes=5)
#     habits = Habit.objects.filter(time__lte=current_time.time(), time__gte=current_time_less.time())
#
#     for habit in habits:
#         user_tg = habit.user.tg_chat_id
#         message = f"Я буду {habit.action} в {habit.time} в {habit.place}"
#         send_telegram_message(user_tg, message)
