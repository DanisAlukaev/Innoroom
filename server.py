import os

from aiogram import Bot, Dispatcher, executor

import debts
import queues
import users

# import environment variable
BOT_TOKEN = os.environ["BOT_TOKEN"]
# initialize the Innoroom bot
bot = Bot(BOT_TOKEN, parse_mode="HTML")
# create a dispatcher
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer(
        "Hello, use /help to see my functionalities.\n"
        "Powered by aiogram.")


# TODO: accept requests to join to users list
# TODO: include debts and services to /me
@dp.message_handler(commands=['help'])
async def help_message(message):
    await message.answer(
        "Telegram-bot for the daily routine of our room in the dormitories of Innopolis.\n\n"
        "You can control me by sending these commands:\n\n"
        "<b>Profile control</b>\n"
        "/register - register in the chat bot\n"
        "/me - get information about me\n"
        "/update_me - update an account\n"
        "/leave - leave bot\n\n"
        "<b>Queues</b>\n"
        "/create_queue <b>title</b> - сreate new queue\n"
        "/remove_queue <b>title</b> - remove the queue\n"
        "/join_queue <b>title</b> - join the queue\n"
        "/quit_queue <b>title</b> - quit the queue\n"
        "/get_queues - get existing queues\n"
        "/my_queues - get my queues\n"
        "/current_user <b>title</b> - get a user whose turn is it now\n"
        "/next_user <b>title</b> - pass turn to next user\n"
        "/skip <b>title</b> - skip your turn\n"
        "/get_states - get states of all queues\n\n"
        "<b>Debts</b>\n"
        "/give <b>money</b> <b>username</b> [...] - give money to user(s) with specified alias(es)\n"
        "/my_debts - get your debts\n"
        "/my_services - get your services\n"
        "/share <b>money</b> - share debt between all users\n"
    )


@dp.message_handler(commands=['register'])
async def register(message):
    reply = users.register(message)
    await message.answer(reply)


@dp.message_handler(commands=['me'])
async def me(message):
    reply = users.me(message)
    await message.answer(reply)


@dp.message_handler(commands=['update_me'])
async def update_me(message):
    reply = users.update_me(message)
    await message.answer(reply)


@dp.message_handler(commands=['leave'])
async def leave(message):
    reply = queues.leave(message)
    await message.answer(reply)


@dp.message_handler(commands=['create_queue'])
async def create_queue(message):
    reply = queues.create_queue(message)
    await message.answer(reply)


@dp.message_handler(commands=['join_queue'])
async def join_queue(message):
    reply = queues.join_queue(message)
    await message.answer(reply)


@dp.message_handler(commands=['quit_queue'])
async def quit_queue(message):
    reply = queues.quit_queue(message)
    await message.answer(reply)


@dp.message_handler(commands=['remove_queue'])
async def remove_queue(message):
    reply = queues.remove_queue(message)
    await message.answer(reply)


@dp.message_handler(commands=['get_queues'])
async def get_queues(message):
    reply = queues.get_queues(message)
    await message.answer(reply)


@dp.message_handler(commands=['my_queues'])
async def my_queues(message):
    reply = queues.my_queues(message)
    await message.answer(reply)


@dp.message_handler(commands=['current_user'])
async def current_user(message):
    reply = queues.current_user(message)
    await message.answer(reply)


@dp.message_handler(commands=['next_user'])
async def next_user(message):
    reply = queues.next_user(message)
    await message.answer(reply)


@dp.message_handler(commands=['skip'])
async def skip(message):
    reply = queues.skip(message)
    await message.answer(reply)


@dp.message_handler(commands=['get_states'])
async def get_states(message):
    reply = queues.get_states(message)
    await message.answer(reply)


@dp.message_handler(commands=['give'])
async def give(message):
    reply = debts.give(message)
    await message.answer(reply)


@dp.message_handler(commands=['my_debts'])
async def get_my_debts(message):
    reply = debts.get_my_debts(message)
    await message.answer(reply)


@dp.message_handler(commands=['my_services'])
async def get_my_services(message):
    reply = debts.get_my_services(message)
    await message.answer(reply)


@dp.message_handler(commands=['share'])
async def share(message):
    reply = debts.share(message)
    await message.answer(reply)


if __name__ == "__main__":
    # run the bot
    executor.start_polling(dp, skip_updates=True)
