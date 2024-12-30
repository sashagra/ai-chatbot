import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from ai_chatbot.config import BOT_TOKEN

users = {}

def is_registered(id:int) -> bool:
    return id in users

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if is_registered(int(message.from_user.id)):
        await message.answer("Команда /new начнет диалог заново. Первым сообщением введите описание агента. \
Если набрать меньше 10 символов, диалог начнется с дефолтным агентом")
    else:
        await message.answer("Привет! Чтобы общаться с ботом введи секретную команду.")


@dp.message(Command("topsecret"))
async def register_user(message: types.Message):
    if is_registered(int(message.from_user.id)):
        await message.answer("Вы уже зарегистрировались ранее! Повторно вводить команду не тебуется")
    else:
        await message.answer("Вы прошли регистрацию, можете общаться с ботом. Первым сообщением введите описание агента. \
Если набрать меньше 10 символов, диалог начнется с дефолтным агентом. Команда /new сбросит диалог")

async def main():
    await dp.start_polling(bot)

def start():
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())
