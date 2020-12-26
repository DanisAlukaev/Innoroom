from bot import bot, dispatcher

from aiogram.types import Message
from config import admin_id


async def send_to_admin(dispatcher):
    await bot.send_message(chat_id=admin_id, text="The bot was launched.")


# get message from the dispatcher
@dispatcher.message_handler()
async def echo(message: Message):
    text = f"Hello, you've just wrote '{message.text}'."
    # await bot.send_message(chat_id=message.from_user.id, text=text)
    await message.answer(text=text)
