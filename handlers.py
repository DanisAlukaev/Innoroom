import random

import logging
from aiogram import types
from asyncpg import Record
from asyncpg.exceptions import UniqueViolationError

from misc import bot, dp
from config import administrators

from modules.users import auxiliary, join_requests, profile, interaction_with_bot
from modules.queues import manage_queues


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer(
        "Hello, use /help to see my functionalities.\n"
        "Powered by aiogram.")


@dp.message_handler(commands=['help'])
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


# Profile
@dp.message_handler(commands=['update_me'])
async def update_me(message):
    reply = await profile.update_me(message)
    await message.answer(reply)


# Interaction with bot
@dp.message_handler(commands=['join_bot'])
async def join_bot(message):
    reply = await interaction_with_bot.join_bot(message)
    await message.answer(reply)


@dp.message_handler(commands=['leave'])
@authorization
async def leave(message):
    reply = await interaction_with_bot.leave(message)
    await message.answer(reply)


# Requests
@dp.message_handler(commands=['accept'])
async def accept(message):
    if message['from']['id'] not in administrators:
        reply = 'Allowed only for administrators.'
    else:
        reply = await join_requests.accept(message)
    await message.answer(reply)


@dp.message_handler(commands=['decline'])
async def decline(message):
    if message['from']['id'] not in administrators:
        reply = 'Allowed only for administrators.'
    else:
        reply = await join_requests.decline(message)
    await message.answer(reply)


@dp.message_handler(commands=['all_requests'])
async def all_requests(message):
    if message['from']['id'] not in administrators:
        reply = 'Allowed only for administrators.'
    else:
        reply = await join_requests.all_requests(message)
    await message.answer(reply)


@dp.message_handler(commands=['remove'])
async def remove(message):
    if message['from']['id'] not in administrators:
        reply = 'Allowed only for administrators.'
    else:
        reply = await join_requests.remove_user(message)
    await message.answer(reply)


# Manage
@dp.message_handler(commands=['create_queue'])
@authorization
async def create_queue(message):
    reply = await manage_queues.create_queue(message)
    await message.answer(reply)


@dp.message_handler(commands=['join_queue'])
@authorization
async def join_queue(message):
    reply = await manage_queues.join_queue(message)
    await message.answer(reply)


@dp.message_handler(commands=['remove_queue'])
@authorization
async def remove_queue(message):
    reply = await manage_queues.remove_queue(message)
    await message.answer(reply)


@dp.message_handler(commands=['get_queues'])
@authorization
async def get_queues(message):
    reply = await manage_queues.get_queues(message)
    await message.answer(reply)


@dp.message_handler(commands=['my_queues'])
@authorization
async def my_queues(message):
    reply = await manage_queues.my_queues(message)
    return await message.reply(reply)


@dp.message_handler(commands=['get_states'])
@authorization
async def get_states(message):
    reply = await manage_queues.get_states(message)
    await message.answer(reply)


@dp.message_handler(commands=['current_user'])
@authorization
async def current_user(message):
    reply = await manage_queues.current_user(message)
    await message.answer(reply)


@dp.message_handler(commands=['next_user'])
@authorization
async def next_user(message):
    reply = await manage_queues.next_user(message)
    await message.answer(reply)


@dp.message_handler(commands=['skip'])
@authorization
async def skip(message):
    reply = await manage_queues.skip(message)
    await message.answer(reply)


@dp.message_handler(commands=['quit_queue'])
@authorization
async def quit_queue(message):
    reply = await manage_queues.quit_queue(message)
    await message.answer(reply)
