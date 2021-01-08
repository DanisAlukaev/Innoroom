from misc import queries
from modules.users import auxiliary
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
    for request in requests:
        aliases += '• @' + request['alias'] + '\n'

    if not aliases:
        message_all_requests = 'There are no pending requests.'
    else:
        message_all_requests = '<b>Current requests:</b>\n' + aliases
    return message_all_requests


async def accept(message):
    """
    Accept request(s) to join of specified users.

    :param message: user's message.
    :return: reply.
    """
    # get name of user
    name = message['from']['first_name']

    if re.fullmatch(r'/accept( @\w+)+', message['text'].replace('\n', '')):
        # message is properly formatted

        # get parsed aliases and aliases that were failed to validate
        aliases = message['text'].replace('@', '').split(' ')[1:]
        aliases, fail_validation, fail_validation_str = await auxiliary.check_presence_requests(aliases)

        if len(fail_validation) == 0:
            # all aliases are in requests list

            message_accept = name + ', you have added new user(s)\n'
            for alias in aliases:
                # accept request
                await queries.accept_request(alias)
                message_accept += '• @' + alias + '\n'
        else:
            # some aliases fail validation
            message_accept = 'User(s) with alias(es) ' + fail_validation_str + 'do(es) not have pending request(s).'
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
    # get name of user
    name = message['from']['first_name']

    if re.fullmatch(r'/decline( @\w+)+', message['text'].replace('\n', '')):
        # message is properly formatted

        # get parsed aliases and aliases that were failed to validate
        aliases = message['text'].replace('@', '').split(' ')[1:]
        aliases, fail_validation, fail_validation_str = await auxiliary.check_presence_requests(aliases)

        if len(fail_validation) == 0:
            # all aliases are in requests list

            message_decline = name + ', you have declined request(s) of \n'
            for alias in aliases:
                # remove request
                await queries.remove_user_by_alias(alias)
                message_decline += '• @' + alias + '\n'
        else:
            # some aliases fail validation
            message_decline = 'User(s) with alias(es) ' + fail_validation_str + 'do(es) not have pending request(s).'
    else:
        # message fails to parse
        message_decline = 'Message does not match the required format. Check rules in /help.'
    return message_decline


async def remove_user(message):
    """
    Remove user of the bot.

    :param message: user's message.
    :return: reply.
    """
    # get name of user
    name = message['from']['first_name']

    if re.fullmatch(r'/remove( @\w+)+', message['text'].replace('\n', '')):
        # message is properly formatted

        # get parsed aliases and aliases that were failed to validate
        aliases = message['text'].replace('@', '').split(' ')[1:]
        aliases, fail_verification, fail_verification_str = await auxiliary.check_presence_users(aliases)

        if len(fail_verification) == 0:
            # all aliases are in users list

            message_remove_user = name + ', you have removed user(s)\n'
            for alias_ in aliases:
                # remove from the list of users
                await queries.remove_user_by_alias(alias_)
                # remove user from all queues
                # TODO: remove from all queues
                message_remove_user += '• @' + alias_ + '\n'
        else:
            # some aliases fail validation
            message_remove_user = 'User(s) with alias(es) ' + fail_verification_str + 'is(are) not user(s) of the bot.'
    else:
        # message fails to parse
        message_remove_user = 'Message does not match the required format. Check rules in /help.'
    return message_remove_user
