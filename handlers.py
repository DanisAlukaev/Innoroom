from misc import dp
from config import administrators

from modules.users import auxiliary, requests, profile, interact
from modules.queues import manage, information as information_queues
from modules.finances import exchange, information as information_finances


async def throttling(*args, **kwargs):
    message = args[0]
    await message.answer('Throttled.')


@dp.message_handler(commands=['start'])
@dp.throttled(throttling, rate=1)
async def start_message(message):
    await message.answer(
        "Hello, use /help to see my functionalities.\n"
        "Powered by aiogram.")


@dp.message_handler(commands=['help'])
@dp.throttled(throttling, rate=1)
async def help_message(message):
    await message.answer(
        "Telegram-bot for the daily routine of our room in the dormitories of Innopolis.\n\n"
        "You can control me by sending these commands:\n\n"
        "<b>Manage bot</b> (only for administrators)\n"
        "/accept <b>username</b> [...] - accept request(s) to join\n"
        "/decline <b>username</b> [...] - decline request(s) to join\n"
        "/all_requests - get all pending requests to join\n"
        "/remove <b>username</b> [...] - remove user(s)\n\n"
        "<b>Profile control</b>\n"
        "/join_bot - send request to join\n"
        "/me - get user information\n"
        "/update_me - automatically update your name, surname, username\n"
        "/leave - leave bot\n\n"
        "<b>Queues</b>\n"
        "/create_queue <b>title</b> - сreate new queue\n"
        "/remove_queue <b>title</b> - remove the queue\n"
        "/join_queue <b>title</b> - join the queue\n"
        "/quit_queue <b>title</b> - quit the queue\n"
        "/get_queues - get existing queues\n"
        "/my_queues - get your queues\n"
        "/current_user <b>title</b> - get a user whose turn is it now\n"
        "/next_user <b>title</b> - pass turn to next user\n"
        "/skip <b>title</b> - skip your turn\n"
        "/get_states - get states of all queues\n\n"
        "<b>Debts</b>\n"
        "/give <b>money</b> <b>username</b> [...] - give money to specified user(s)\n"
        "/my_debts - get your debts\n"
        "/my_services - get your services\n"
        "/share <b>money</b> - share money between all users\n"
    )


def authorization(func):
    """
    Decorator for authorization.
    Check whether sender is in the list of users.
    """

    async def wrapper(message):
        if message['from']['id'] not in (await auxiliary.get_user_ids()):
            return await message.reply('You are not the user of the bot.')
        return await func(message)

    return wrapper


# users.profile

@dp.message_handler(commands=['update_me'])
@dp.throttled(throttling, rate=1)
async def update_me(message):
    reply = await profile.update_me(message)
    await message.answer(reply)


@dp.message_handler(commands=['me'])
@dp.throttled(throttling, rate=1)
@authorization
async def me(message):
    reply = await profile.me(message)
    await message.answer(reply)


# users.interaction_with_bot

@dp.message_handler(commands=['join_bot'])
@dp.throttled(throttling, rate=1)
async def join_bot(message):
    reply = await interact.join_bot(message)
    await message.answer(reply)


@dp.message_handler(commands=['leave'])
@dp.throttled(throttling, rate=1)
@authorization
async def leave(message):
    reply = await interact.leave(message)
    await message.answer(reply)


# users.join_requests

@dp.message_handler(commands=['accept'])
@dp.throttled(throttling, rate=1)
async def accept(message):
    if message['from']['id'] not in administrators:
        reply = 'Allowed only for administrators.'
    else:
        reply = await requests.accept(message)
    await message.answer(reply)


@dp.message_handler(commands=['decline'])
@dp.throttled(throttling, rate=1)
async def decline(message):
    if message['from']['id'] not in administrators:
        reply = 'Allowed only for administrators.'
    else:
        reply = await requests.decline(message)
    await message.answer(reply)


@dp.message_handler(commands=['all_requests'])
@dp.throttled(throttling, rate=1)
async def all_requests(message):
    if message['from']['id'] not in administrators:
        reply = 'Allowed only for administrators.'
    else:
        reply = await requests.all_requests(message)
    await message.answer(reply)


@dp.message_handler(commands=['remove'])
@dp.throttled(throttling, rate=1)
async def remove(message):
    if message['from']['id'] not in administrators:
        reply = 'Allowed only for administrators.'
    else:
        reply = await requests.remove_user(message)
    await message.answer(reply)


# queues.manage_queues

@dp.message_handler(commands=['create_queue'])
@dp.throttled(throttling, rate=1)
@authorization
async def create_queue(message):
    reply = await manage.create_queue(message)
    await message.answer(reply)


@dp.message_handler(commands=['join_queue'])
@dp.throttled(throttling, rate=1)
@authorization
async def join_queue(message):
    reply = await manage.join_queue(message)
    await message.answer(reply)


@dp.message_handler(commands=['remove_queue'])
@dp.throttled(throttling, rate=1)
@authorization
async def remove_queue(message):
    reply = await manage.remove_queue(message)
    await message.answer(reply)


@dp.message_handler(commands=['next_user'])
@dp.throttled(throttling, rate=1)
@authorization
async def next_user(message):
    reply = await manage.next_user(message)
    await message.answer(reply)


@dp.message_handler(commands=['skip'])
@dp.throttled(throttling, rate=1)
@authorization
async def skip(message):
    reply = await manage.skip(message)
    await message.answer(reply)


@dp.message_handler(commands=['quit_queue'])
@dp.throttled(throttling, rate=1)
@authorization
async def quit_queue(message):
    reply = await manage.quit_queue(message)
    await message.answer(reply)


# queues.information

@dp.message_handler(commands=['get_queues'])
@dp.throttled(throttling, rate=1)
@authorization
async def get_queues(message):
    reply = await information_queues.get_queues(message)
    await message.answer(reply)


@dp.message_handler(commands=['my_queues'])
@dp.throttled(throttling, rate=1)
@authorization
async def my_queues(message):
    reply = await information_queues.my_queues(message)
    return await message.reply(reply)


@dp.message_handler(commands=['get_states'])
@dp.throttled(throttling, rate=1)
@authorization
async def get_states(message):
    reply = await information_queues.get_states(message)
    await message.answer(reply)


@dp.message_handler(commands=['current_user'])
@dp.throttled(throttling, rate=1)
@authorization
async def current_user(message):
    reply = await information_queues.current_user(message)
    await message.answer(reply)


# finances.exchange

@dp.message_handler(commands=['give'])
@dp.throttled(throttling, rate=1)
@authorization
async def give(message):
    reply = await exchange.give(message)
    await message.answer(reply)


@dp.message_handler(commands=['share'])
@dp.throttled(throttling, rate=1)
@authorization
async def share(message):
    reply = await exchange.share(message)
    await message.answer(reply)


# finances.information

@dp.message_handler(commands=['my_debts'])
@dp.throttled(throttling, rate=1)
@authorization
async def get_my_debts(message):
    reply = await information_finances.get_my_debts(message)
    await message.answer(reply)


@dp.message_handler(commands=['my_services'])
@dp.throttled(throttling, rate=1)
@authorization
async def get_my_services(message):
    reply = await information_finances.get_my_services(message)
    await message.answer(reply)
