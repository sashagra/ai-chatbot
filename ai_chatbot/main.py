import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
import re

from ai_chatbot.config import BOT_TOKEN
from ai_chatbot.chatgpt import ChatGptDialogs

d = ChatGptDialogs()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def escape_markdown(text):
    """Экранирует специальные символы для Markdown."""
    return re.sub(r'([_*[\]()~`>)])', r'\\\1', text)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if d.is_registrated(int(message.from_user.id)):
        await message.answer("Команда /new начнет диалог заново. Первым сообщением введите описание агента. \
Если набрать меньше 10 символов, диалог начнется с дефолтным агентом")
    else:
        await message.answer("Привет! Чтобы общаться с ботом введи секретную команду.")

@dp.message(Command("new"))
async def reset_dialog(message: types.Message):
    if not d.is_registrated(int(message.from_user.id)): return
    await message.answer(d.reset_dialog(message.from_user.id))


@dp.message(Command("topsecret"))
async def register_user(message: types.Message):
    user_id = int(message.from_user.id)
    await message.answer(d.user_register(user_id))

@dp.message(F.text)
async def dialog(message: types.Message):
    print(message)
    await message.answer(
                d.send_to_openai(int(message.from_user.id), escape_markdown(message.text)),
                parse_mode=ParseMode.MARKDOWN
    )


async def main():
    await dp.start_polling(bot)

def start():
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())
