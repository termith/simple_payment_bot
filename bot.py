import os
import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, executor

import schedule

TOKEN = os.getenv('YANDEX_SPANISH_BOT_TOKEN')
CHECK_PERIOD = 3600 * 24
NOTIFICATION_OFFSET = 9

logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler()
async def echo(message):
    logging.info(f'Message was "{message.text}"')
    await message.answer(message.text)


def schedule_task(loop, task):
    loop.create_task(task())


async def create_payment():
    while True:
        print('Call later')
        # await asyncio.sleep(CHECK_PERIOD)
        await asyncio.sleep(10)

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
    loop.call_later((datetime.now() - start_date).seconds, schedule_task, loop, create_payment)
    executor.start_polling(dispatcher, skip_updates=True, loop=loop)
