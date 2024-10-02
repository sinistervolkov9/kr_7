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


@app.task
def send_telegram_notification():
    now = timezone.localtime()
    # print(f'now = {now}')

    habits = Habit.objects.filter(status='active', user__telegram_chat_id__isnull=False)

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
        # print(f'({user}) habit_start = {habit_start}')

        # Приводим last_notification_time к локальной временной зоне или используем время старта для первого уведомления
        last_notification_time = timezone.localtime(
            habit.last_notification_time) if habit.last_notification_time else None

        # Получаем timedelta для периодичности
        period = PERIODICITY_TO_TIMDELTA.get(habit.periodicity, timedelta())
        print(f'({user}) period = {period}')

        # Если уведомлений не было, используем habit_start для первого уведомления
        if not last_notification_time:
            # print(f'({user}) not last_notification_time')
            last_notification_time = habit_start
            if now >= last_notification_time:
                # print(f'({user}) now >= last_notification_time')
                try:
                    # Отправляем уведомление
                    async_to_sync(send_message)(user.telegram_chat_id, message)
                    print(f'({user}) SEND NOTIFICATION - {message}')

                    # Обновляем habit.last_notification_time
                    habit.last_notification_time = habit_start
                    # print(f'({user}) Обновляем habit.last_notification_time ({habit.last_notification_time})')

                    # Рассчитываем следующее время уведомления
                    next_notification_time = timezone.localtime(habit.last_notification_time) + period
                    # print(f'({user}) Рассчитываем следующее время уведомления')

                    # Если пропущено несколько уведомлений, корректируем next_notification_time
                    while next_notification_time <= now:
                        next_notification_time += period
                        # print(f'({user}) Пропущено несколько уведомлений - корректируем next_notification_time')

                    habit.next_notification_time = next_notification_time
                    # print(f'({user}) habit.next_notification_time - {timezone.localtime(habit.next_notification_time)}')
                    print(f'({user}) Время след. уведомления - {timezone.localtime(habit.next_notification_time)}')
                    habit.save()
                except TelegramForbiddenError:
                    print(f'({user}) Не удалось отправить сообщение пользователю (TelegramForbiddenError)')
            else:
                pass
                # print(f'({user}) now < last_notification_time')
        else:
            last_notification_time = timezone.localtime(habit.last_notification_time)
        # print(f'({user}) last_notification_time = {last_notification_time}')

        # Если next_notification_time еще не установлено или пропущено несколько уведомлений
        if not habit.next_notification_time or timezone.localtime(habit.next_notification_time) >= now:
            # print(f'({user}) not habit.next_notification_time or habit.next_notification_time >= now')
            next_notification_time = last_notification_time + period
            # print(f'({user}) next_notification_time = last_notification_time + period ({next_notification_time})')

            # Проверяем, если следующее уведомление в прошлом, увеличиваем до актуального времени
            while next_notification_time <= now:
                next_notification_time += period
                # print(f'({user}) Увеличиваем следующее уведомление до актуального времени')

            habit.next_notification_time = next_notification_time
            # print(f'({user}) habit.next_notification_time = next_notification_time ({timezone.localtime(habit.next_notification_time)})')
            print(f'({user}) Время след. уведомления - {timezone.localtime(habit.next_notification_time)}')
            habit.save()
        else:
            pass
            # print(f'({user}) habit.next_notification_time >= now ({timezone.localtime(habit.next_notification_time)})')

        # Проверяем, если текущее время больше или равно следующему времени уведомления
        if now >= timezone.localtime(habit.next_notification_time):
            # print(f'({user}) now >= habit.next_notification_time')
            try:
                # Отправляем уведомление
                async_to_sync(send_message)(user.telegram_chat_id, message)
                print(f'({user}) SEND NOTIFICATION - {message}')

                # Обновляем habit.last_notification_time
                habit.last_notification_time = now
                # print(f'({user}) Обновляем habit.last_notification_time ({habit.last_notification_time})')

                # Рассчитываем следующее время уведомления
                next_notification_time = timezone.localtime(habit.next_notification_time) + period
                # print(f'({user}) Рассчитываем следующее время уведомления')

                # Если пропущено несколько уведомлений, корректируем next_notification_time
                while next_notification_time <= now:
                    next_notification_time += period
                    # print(f'({user}) Пропущено несколько уведомлений - корректируем next_notification_time')

                habit.next_notification_time = next_notification_time
                # print(f'({user}) habit.next_notification_time - {timezone.localtime(habit.next_notification_time)}')
                print(f'({user}) Время след. уведомления - {timezone.localtime(habit.next_notification_time)}')
                habit.save()

            except TelegramForbiddenError:
                print(f'({user}) Не удалось отправить сообщение пользователю (TelegramForbiddenError)')
        else:
            pass
            # print(f'({user}) now < habit.next_notification_time')
