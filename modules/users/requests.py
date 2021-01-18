from misc import queries
from modules.users import auxiliary
import config
import re


async def all_requests(message):
    """
    Return all requests to join.

    :param message: user's message.
    :return: reply.
    """
    # get all users with pending requests
    requests = await queries.get_requests()
    # string with aliases of users with pending requests
    aliases = ''
    # get string requests
    for request in requests:
        aliases += '• @' + request['alias'] + '\n'
    message_all_requests = 'There are no pending requests.' if not aliases else '<b>Current requests:</b>\n' + aliases
    return message_all_requests


async def accept(message):
    """
    Accept request(s) to join of specified users.

    :param message: user's message.
    :return: reply.
    """
    # get name of user
    name = message['from']['first_name']

    if not re.fullmatch(r'/accept( @\w+)+', message['text'].replace('\n', '')):
        # if message fails to parse
        return 'Message does not match the required format. Check rules in /help.'

    # get parsed aliases and aliases that were failed to validate
    aliases = message['text'].replace('@', '').split(' ')[1:]
    aliases, fail_validation, fail_validation_str = await auxiliary.check_presence_requests(aliases)

    if len(fail_validation) != 0:
        # some aliases fail validation
        return 'User(s) with alias(es) ' + fail_validation_str + 'do(es) not have pending request(s).'

    message_accept = name + ', you have added new user(s):\n'
    for alias in aliases:
        # update table users with pending request
        await queries.accept_request(alias)
        # id of user in table users
        response = await queries.get_user_by_alias(alias)
        if not response:
            return 'Error.'
        id_new_user = response['id']
        # get all users
        users = await queries.get_users()

        # update table debts
        for user in users:
            if user['id'] != id_new_user:
                # create bidirectional debt entry
                id_old_user = user['id']
                await queries.create_zero_debt(id_new_user, id_old_user)
                await queries.create_zero_debt(id_old_user, id_new_user)
        message_accept += '• @' + alias + '\n'
    return message_accept


async def decline(message):
    """
    Decline request(s) to join of specified users.

    :param message: user's message.
    :return: reply.
    """
    # get name of user
    name = message['from']['first_name']

    if not re.fullmatch(r'/decline( @\w+)+', message['text'].replace('\n', '')):
        # message fails to parse
        return 'Message does not match the required format. Check rules in /help.'

    # get parsed aliases and aliases that were failed to validate
    aliases = message['text'].replace('@', '').split(' ')[1:]
    aliases, fail_validation, fail_validation_str = await auxiliary.check_presence_requests(aliases)

    if len(fail_validation) != 0:
        # some aliases fail validation
        return 'User(s) with alias(es) ' + fail_validation_str + 'do(es) not have pending request(s).'

    message_decline = name + ', you have declined request(s) of \n'
    for alias in aliases:
        # remove request
        await queries.remove_user_by_alias(alias)
        message_decline += '• @' + alias + '\n'
    return message_decline


async def remove_user(message):
    """
    Remove user of the bot.

    :param message: user's message.
    :return: reply.
    """
    # get name of user
    name = message['from']['first_name']

    if not re.fullmatch(r'/remove( @\w+)+', message['text'].replace('\n', '')):
        # message fails to parse
        return 'Message does not match the required format. Check rules in /help.'

    # get parsed aliases and aliases that were failed to validate
    aliases = message['text'].replace('@', '').split(' ')[1:]
    aliases, fail_verification, fail_verification_str = await auxiliary.check_presence_users(aliases)

    if len(fail_verification) != 0:
        # some aliases fail validation
        return 'User(s) with alias(es) ' + fail_verification_str + 'is(are) not user(s) of the bot.'

    message_remove_user = name + ', you have removed user(s)\n'
    for alias_ in aliases:
        # remove from the list of users
        await queries.remove_user_by_alias(alias_)
        message_remove_user += '• @' + alias_ + '\n'
    return message_remove_user


async def new_admin(message):
    """
    Remove user of the bot.

    :param message: user's message.
    :return: reply.
    """
    if not re.fullmatch(r'/new_admin @\w+', message['text'].replace('\n', '')):
        # message fails to parse
        return 'Message does not match the required format. Check rules in /help.'

    # get request
    request_message = message['text'].replace('@', '').split(' ')
    # get alias of user to be removed
    alias = request_message[1]
    # get user to be removed
    user = await queries.get_user_by_alias(alias)
    if not user:
        return 'There is no users with alias ' + alias + '.'
    uid = user['uid']

    if not uid not in config.administrators:
        return 'User with specified alias is already an administrator.'
    config.administrators.append(uid)
    message_remove_user = '@' + alias + ', you are now an administrator of the bot.'
    return message_remove_user
