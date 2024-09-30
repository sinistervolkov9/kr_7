import asyncio
from aiogram.exceptions import TelegramForbiddenError
from celery import shared_task
from .models import Habit
from habits.telegram import send_message
from asgiref.sync import async_to_sync
from config.celery import app
from django.utils import timezone
from datetime import datetime, timedelta
from .models import PERIODICITY_TO_TIMDELTA


@shared_task
def habits_activator():
    now = timezone.now()
    habits = Habit.objects.filter(status='created')

    print("habits_activator")

    for habit in habits:
        if habit.should_be_active():
            habit.status = 'active'
            habit.save()

            print(f'Привычка {habit.action} активирована!')
            # send_telegram_notification.delay(habit.user.id, f"Привычка {habit.action} активирована!")


@app.task
def send_telegram_notification():
    now = timezone.localtime()
    habits = Habit.objects.filter(status='active', user__telegram_chat_id__isnull=False)

    print(f'now = {now}')

    for habit in habits:
        user = habit.user
        if habit.related_habit:
            message = (f"Привет, {habit.user}! "
                       f"Нужно выполнить '{habit.action}', "
                       f"в месте '{habit.place}', "
                       f"а за это ты можешь выполнить '{habit.related_habit}'!")
        elif habit.reward:
            message = (f"Привет, {habit.user}! "
                       f"Нужно выполнить '{habit.action}', "
                       f"в месте '{habit.place}', "
                       f"а за это ты получишь награду '{habit.reward}'!")
        else:
            message = (f"Привет, {habit.user}! "
                       f"Нужно выполнить '{habit.action}', "
                       f"в месте '{habit.place}'!")

        # Приводим время старта привычки к локальному времени
        habit_start = timezone.make_aware(datetime.combine(habit.start_date, habit.time),
                                          timezone.get_current_timezone())
        print(f'habit_start = {habit_start} ({user})')

        # Приводим last_notification_time к локальной временной зоне или используем время старта
        last_notification_time = timezone.localtime(
            habit.last_notification_time) if habit.last_notification_time else habit_start
        print(f'last_notification_time = {last_notification_time} ({user})')

        # Получаем timedelta для периодичности
        period = PERIODICITY_TO_TIMDELTA.get(habit.periodicity, timedelta())
        print(f'period = {period} ({user})')

        # Рассчитываем ближайшее следующее время уведомления
        notification_time = last_notification_time
        # Пока notification_time меньше текущего времени, увеличиваем его
        while notification_time <= now:
            notification_time += period
        print(f'notification_time = {notification_time} ({user})')
        print(f'??? = {notification_time - period}')

        # Если текущее время больше или равно следующему уведомлению
        if now >= notification_time - period:
            try:
                print(f'SEND {user} - {message}')
                async_to_sync(send_message)(user.telegram_chat_id, message)
                habit.last_notification_time = now
                habit.save()
            except TelegramForbiddenError:
                print(f'Не удалось отправить сообщение пользователю {user} (TelegramForbiddenError)')

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
