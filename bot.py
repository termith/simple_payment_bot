import os
import asyncio
import logging
from datetime import datetime, timedelta, date

import aiosqlite
from aiogram import Bot, Dispatcher, executor

import schedule

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


async def create_payment():
    while True:
        print('Call later')
        # await asyncio.sleep(CHECK_PERIOD)
        await asyncio.sleep(10)


@dispatcher.message_handler(commands=['next_payment'])
async def next_payment(message):
    c = await db_connection.execute(f'SELECT payment_date FROM payments where payment_date > {date.today().strftime(DATE_FORMAT)} order by payment_date desc')
    r = await c.fetchone()
    await message.answer(r)


if __name__ == '__main__':
    if schedule.START_DATE is not None:
        start_date = datetime.strptime(schedule.START_DATE, schedule.DATE_FORMAT)
        start_date += timedelta(hours=NOTIFICATION_OFFSET)
    else:
        # Находим ближайший к сегодняшнему день занятия
        today = datetime.now().weekday()
        min_offset = 7
        for day in schedule.CLASS_DAYS:
            offset = (day - today) % 7
            if offset < min_offset:
                min_offset = offset
        start_date = datetime.today() + timedelta(days=min_offset)
        start_date -= timedelta(hours=start_date.hour, minutes=start_date.minute, seconds=start_date.second)
        start_date += timedelta(hours=NOTIFICATION_OFFSET)

    loop = asyncio.get_event_loop()
    loop.create_task(create_db_connection())
    loop.call_later((datetime.now() - start_date).seconds,
                    lambda loop_, task_: loop_.create_task(task_()), loop, create_payment)
    executor.start_polling(dispatcher, skip_updates=True, loop=loop)
