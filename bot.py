import asyncio

from aiogram import executor

from config import admin_id
from misc import bot, create_db


async def on_shutdown(dp):
    await bot.close()


async def on_startup(dp):
    await create_db()
    await bot.send_message(admin_id, "The bot is running...")


if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp, skip_updates=True, on_shutdown=on_shutdown, on_startup=on_startup)
