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
# id of a bot's admin
admin_uid = [481338688]


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer(
        "Hello, use /help to see my functionalities.\n"
        "Powered by aiogram.")


# TODO: include debts and services to /me
@dp.message_handler(commands=['help'])
async def help_message(message):
    await message.answer(
        "Telegram-bot for the daily routine of our room in the dormitories of Innopolis.\n\n"
        "You can control me by sending these commands:\n\n"
        "<b>Manage</b> (only for administrators)\n"
        "/accept <b>username</b> [...] - accept request(s) of user(s)\n"
        "/all_requests - get all pending requests\n"
        "/decline <b>username</b> [...] - decline request(s) of user(s)\n\n"
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


def authorization(func):
    """
    Decorator for authorization.
    Check whether sender is in the list of users.
    """

    async def wrapper(message):
        if message['from']['id'] not in users.users.keys():
            return await message.reply('Access Denied.')
        return await func(message)

    return wrapper


@dp.message_handler(commands=['accept'])
async def accept(message):
    if message['from']['id'] not in admin_uid:
        reply = 'Allowed only for administrators.'
    else:
        reply = users.accept(message)
    await message.answer(reply)


@dp.message_handler(commands=['decline'])
async def decline(message):
    if message['from']['id'] not in admin_uid:
        reply = 'Allowed only for administrators.'
    else:
        reply = users.decline(message)
    await message.answer(reply)


@dp.message_handler(commands=['all_requests'])
async def all_requests(message):
    if message['from']['id'] not in admin_uid:
        reply = 'Allowed only for administrators.'
    else:
        reply = users.all_requests(message)
    await message.answer(reply)


@dp.message_handler(commands=['register'])
async def register(message):
    reply = users.register(message)
    await message.answer(reply)


@dp.message_handler(commands=['me'])
@authorization
async def me(message):
    reply = users.me(message)
    await message.answer(reply)


@dp.message_handler(commands=['update_me'])
@authorization
async def update_me(message):
    reply = users.update_me(message)
    await message.answer(reply)


@dp.message_handler(commands=['leave'])
@authorization
async def leave(message):
    reply = queues.leave(message)
    await message.answer(reply)


@dp.message_handler(commands=['create_queue'])
@authorization
async def create_queue(message):
    reply = queues.create_queue(message)
    await message.answer(reply)


@dp.message_handler(commands=['join_queue'])
@authorization
async def join_queue(message):
    reply = queues.join_queue(message)
    await message.answer(reply)


@dp.message_handler(commands=['quit_queue'])
@authorization
async def quit_queue(message):
    reply = queues.quit_queue(message)
    await message.answer(reply)


@dp.message_handler(commands=['remove_queue'])
@authorization
async def remove_queue(message):
    reply = queues.remove_queue(message)
    await message.answer(reply)


@dp.message_handler(commands=['get_queues'])
@authorization
async def get_queues(message):
    reply = queues.get_queues(message)
    await message.answer(reply)


@dp.message_handler(commands=['my_queues'])
@authorization
async def my_queues(message):
    reply = queues.my_queues(message)
    await message.answer(reply)


@dp.message_handler(commands=['current_user'])
@authorization
async def current_user(message):
    reply = queues.current_user(message)
    await message.answer(reply)


@dp.message_handler(commands=['next_user'])
@authorization
async def next_user(message):
    reply = queues.next_user(message)
    await message.answer(reply)


@dp.message_handler(commands=['skip'])
@authorization
async def skip(message):
    reply = queues.skip(message)
    await message.answer(reply)


@dp.message_handler(commands=['get_states'])
@authorization
async def get_states(message):
    reply = queues.get_states(message)
    await message.answer(reply)


@dp.message_handler(commands=['give'])
@authorization
async def give(message):
    reply = debts.give(message)
    await message.answer(reply)


@dp.message_handler(commands=['my_debts'])
@authorization
async def get_my_debts(message):
    reply = debts.get_my_debts(message)
    await message.answer(reply)


@dp.message_handler(commands=['my_services'])
@authorization
async def get_my_services(message):
    reply = debts.get_my_services(message)
    await message.answer(reply)


@dp.message_handler(commands=['share'])
@authorization
async def share(message):
    reply = debts.share(message)
    await message.answer(reply)


if __name__ == "__main__":
    # run the bot
    executor.start_polling(dp, skip_updates=True)
