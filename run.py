import asyncio
from aiogram import Bot, Dispatcher
import logging

from app.client import client
from app.admin import admin
from app.database.models import init_models


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')


async def main():
    bot = Bot(token='8202917082:AAFWwE7bS60UnVbxYwgSKf6ZOywLo_QMlBI')
    dp = Dispatcher()
    dp.include_routers(client, admin)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    await dp.start_polling(bot)


async def startup(dispatcher: Dispatcher):
    await init_models()
    logging.info('Bot started up...')


async def shutdown(dispatcher: Dispatcher):
    logging.info('Bot shutting down...')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Bot stopped')