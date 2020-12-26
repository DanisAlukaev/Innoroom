import asyncio
from aiogram import Bot, Dispatcher, executor

from config import BOT_TOKEN

# create an asynchronous thread
loop = asyncio.get_event_loop()
# initialize the Innoroom bot
bot = Bot(BOT_TOKEN, parse_mode="HTML")
# create a dispatcher
dispatcher = Dispatcher(bot, loop=loop)

if __name__ == "__main__":
    from handlers import dispatcher, send_to_admin
    # run the bot
    executor.start_polling(dispatcher, on_startup=send_to_admin)
