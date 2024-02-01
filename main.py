from aiogram.utils import executor
import logging
from create_bot import dp
from handlers import users
import os

logging.basicConfig(level=logging.INFO)
users.register_handlers(dp)


async def on_startup(_):
    if not os.path.exists('cookies'):
        os.mkdir('cookies')
    if not os.path.exists('files'):
        os.mkdir('files')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
