import random

import logging
from aiogram import types
from asyncpg import Record
from asyncpg.exceptions import UniqueViolationError

from misc import bot, dp
from config import administrators

from modules.users import auxiliary, requests


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
            return await message.reply('Access Denied.')
        return await func(message)

    return wrapper


@dp.message_handler(commands=['join_bot'])
async def join_bot(message):
    reply = await requests.join_bot(message)
    await message.answer(reply)


@dp.message_handler(commands=['accept'])
async def accept(message):
    if message['from']['id'] not in administrators:
        reply = 'Allowed only for administrators.'
    else:
        reply = await requests.accept(message)
    await message.answer(reply)


@dp.message_handler(commands=['decline'])
async def decline(message):
    if message['from']['id'] not in administrators:
        reply = 'Allowed only for administrators.'
    else:
        reply = await requests.decline(message)
    await message.answer(reply)


@dp.message_handler(commands=['all_requests'])
async def all_requests(message):
    if message['from']['id'] not in administrators:
        reply = 'Allowed only for administrators.'
    else:
        reply = await requests.all_requests(message)
    await message.answer(reply)


@dp.message_handler(commands=['update_me'])
async def update_me(message):
    reply = await requests.update_me(message)
    await message.answer(reply)
