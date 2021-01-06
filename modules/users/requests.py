from misc import queries
from modules.users import auxiliary
import re
import logging


async def join_bot(message):
    """
    Save sender request as pending.

    :param message: user's message.
    :return: reply.
    """
    # get identification, name and surname of a sender
    uid = message['from']['id']
    name = message['from']['first_name']
    surname = message['from']['last_name']

    # bot works only with users that have usernames in telegram
    if not message['from']['username']:
        message_add_user = name + ' ' + surname + ', you should have username in Telegram.'
        return message_add_user

    # get username
    alias = message['from']['username']

    if uid in (await auxiliary.get_user_ids()):
        # sender is already in the list of users
        message_add_user = '@' + alias + ', you are already in the list of users.'
    elif uid in (await auxiliary.get_request_ids()):
        # sender has already sent request
        message_add_user = '@' + alias + ', your request has not been processed yet.'
    else:
        # create new request
        success = await queries.add_request(uid, alias, name, surname)
        if success:
            # new request was created
            profile = await auxiliary.user_data_to_string(uid)
            message_add_user = '@' + alias + ", your request was successfully sent.\n\n" + profile
        else:
            message_add_user = 'Something went wrong...'
    return message_add_user


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
    for request in requests:
        aliases += '• @' + request['alias'] + '\n'

    if not aliases:
        message_all_requests = 'There are no pending requests.'
    else:
        message_all_requests = '<b>Current requests</b>\n' + aliases
    return message_all_requests


async def accept(message):
    """
    Accept request(s) to join of specified users.

    :param message: user's message.
    :return: reply.
    """
    # get alias of user
    alias = message['from']['username']

    if re.fullmatch(r'/accept( @\w+)+', message['text'].replace('\n', '')):
        # message is properly formatted

        # get parsed aliases and aliases that were failed to validate
        aliases, fail_validation, fail_validation_str = await auxiliary.check_presence_requests(message)

        if len(fail_validation) == 0:
            # all aliases are in requests list
            message_accept = '@' + alias + ', you have added new user(s)\n'
            for alias in aliases:
                # accept request
                await queries.accept_request(alias)
                message_accept += '• @' + alias + '\n'
        else:
            # some aliases fail validation
            message_accept = 'User with alias(es) ' + fail_validation_str + "didn't send joining request in bot."
    else:
        # message fails to parse
        message_accept = 'Message does not match the required format. Check rules in /help.'
    return message_accept


async def decline(message):
    """
    Decline request(s) to join of specified users.

    :param message: user's message.
    :return: reply.
    """
    # get alias of user
    alias = message['from']['username']

    if re.fullmatch(r'/decline( @\w+)+', message['text'].replace('\n', '')):
        # message is properly formatted

        # get parsed aliases and aliases that were failed to validate
        aliases, fail_validation, fail_validation_str = await auxiliary.check_presence_requests(message)

        if len(fail_validation) == 0:
            # all aliases are in requests list
            message_decline = '@' + alias + ', you have declined request(s) of \n'
            for alias in aliases:
                # remove request
                await queries.decline_request(alias)
                message_decline += '• @' + alias + '\n'
        else:
            # some aliases fail validation
            message_decline = 'User with alias(es) ' + fail_validation_str + 'did not send joining request in bot.'
    else:
        # message fails to parse
        message_decline = 'Message does not match the required format. Check rules in /help.'
    return message_decline


async def update_me(message):
    """
    Update information about the user.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    alias = message['from']['username']
    name = message['from']['first_name']
    surname = message['from']['last_name']

    if len(await queries.get_by_uid(uid)) != 0:
        # user with given id exists

        # update alias, name, surname of user
        await queries.update_alias(alias, uid)
        await queries.update_name(name, uid)
        await queries.update_surname(surname, uid)

        message_change_name = '@' + alias + ', your account was successfully updated.\n\n' + (
            await auxiliary.user_data_to_string(uid))
    else:
        message_change_name = 'Send the request first.'
    return message_change_name
