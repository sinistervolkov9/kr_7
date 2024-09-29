import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command as AiogramCommand
from asgiref.sync import sync_to_async
from users.models import User
from config.settings import TELEGRAM_TOKEN
from aiogram.client.session.aiohttp import AiohttpSession

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


# @dp.message_handler(AiogramCommand('start'))
@dp.message(AiogramCommand('start'))
async def start_command(message: types.Message):
    user, created = await sync_to_async(User.objects.get_or_create)(
        username=message.from_user.username
    )
    user.telegram_chat_id = message.chat.id
    await sync_to_async(user.save)()
    await message.reply("Привет! Я бот, интегрированный в Django через aiogram!")


# async def send_message(chat_id: int, message: str):
#     """Функция для отправки сообщения через бота."""
#     await bot.send_message(chat_id=chat_id, text=message)


async def send_message(chat_id, message):
    async with AiohttpSession() as session:
        bot = Bot(token=TELEGRAM_TOKEN, session=session)
        await bot.send_message(chat_id=chat_id, text=message)


async def run_bot():
    """Запуск polling бота"""
    await dp.start_polling(bot)
