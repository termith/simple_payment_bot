import os

from aiogram import Bot, Dispatcher, executor

token = os.getenv('YANDEX_SPANISH_BOT_TOKEN') or '1259413176:AAFTtsuqZBLXxdjKTKTXZeoJsLumT7tqEr4'


bot = Bot(token)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler()
async def echo(message):
    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
