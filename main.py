import asyncio
import random

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config import config

API_TOKEN = config.token
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

statistic = {
   1: {
        'win': 0,
        'lose': 0
    }
}


@dp.message(Command(commands=['start']))
async def start_command(message: Message):
    await message.answer('Привет, сыграем в игру - я загадываю число от 1 до 3, а ты попытаешься угадать')

@dp.message(Command(commands=['help']))
async def help(message: Message):
    await message.answer('Чтобы посмотреть свою статистику, введите "/statistic".')


@dp.message(Command(commands=['statistic']))
async def get_statistic(message: Message):
    current_user_stats = statistic[message.chat.id]
    await message.answer(f'Побед: {current_user_stats["win"]}\nПоражений: {current_user_stats["lose"]}')
@dp.message()
async def handle_number(message: Message):
    if message.text.isdigit():
        number = random.randint(1, 3)
        chat_id = message.chat.id
        if not chat_id in statistic:
            statistic[chat_id] = {
                'lose': 0,
                'win': 0
            }
        if number == int(message.text):
            await message.answer("Да, вы угадали :-). Я перезагадал число")
            statistic[chat_id]['win'] += 1
        else:
            await message.answer("Нет, вы не угадали :-(. Я перезагадал число")
            statistic[chat_id]['lose'] += 1



async def main():
    try:
        print('Bot started')
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')