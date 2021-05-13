import json
import os
import asyncio
import logging
from datetime import datetime, timedelta, date

import aiosqlite
from aiogram import Bot, Dispatcher, executor, types as ttypes

TOKEN = os.getenv('YANDEX_SPANISH_BOT_TOKEN')
CHECK_PERIOD = 3600 * 24
NOTIFICATION_OFFSET = 9
DATE_FORMAT = "%Y-%m-%d"

logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot)

db_connection = None


async def create_db_connection():
    global db_connection
    db_connection = await aiosqlite.connect('lediludabot.db')


@dispatcher.message_handler(commands="echo")
async def echo(message):
    logging.info(f'Message was "{message.text}"')
    await message.answer(message.text)


@dispatcher.message_handler(commands=['start'])
async def start(message: ttypes.Message):
    assert db_connection is not None, 'You should initialize DB connection first'
    chat_id = message.chat.id
    c = await db_connection.execute('SELECT chat_settings, chat_id FROM chats WHERE tg_chat_id=?', chat_id)
    j = await c.fetchone()
    if not j:
        # https://docs.aiogram.dev/en/latest/examples/finite_state_machine_example.html
        # Первый запуск, нужно сделать настройку
        pass
    else:
        settings = json.loads(j[0][0])
        loop = asyncio.get_event_loop()
        loop.create_task(create_payment(settings['start_date'], j[0][1]))
        loop.create_task(schedule(settings['daysofweek'], settings['period']))


async def schedule(days, period):
    pass


async def create_payment(date, chat_id):
    assert db_connection is not None, 'You should initialize DB connection first'
    await db_connection.execute('INSERT INTO payments (date, chat_id) VALUES (?, ?)', date, chat_id)


@dispatcher.message_handler(regexp='(?:next|last)_payment')
async def next_payment(message: ttypes.Message):
    assert db_connection is not None, 'You should initialize DB connection first'
    sign = '>' if message.get_command() == 'next_payment' else '<'
    c = await db_connection.execute(
        f'SELECT payment_date FROM payments where payment_date {sign} {date.today().strftime(DATE_FORMAT)} order by payment_date desc')
    r = await c.fetchone()
    answer = r[0] if r is not None else '404 not found'
    await message.answer(answer)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(create_db_connection())
    executor.start_polling(dispatcher, skip_updates=True, loop=loop)
