import asyncio
from django.core.management.base import BaseCommand
from habits.telegram import run_bot


class Command(BaseCommand):
    help = 'Запуск Telegram бота'

    def handle(self, *args, **kwargs):
        asyncio.run(run_bot())
