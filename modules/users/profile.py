from misc import queries
from modules.users import auxiliary
import re


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


async def leave(message):
    """
    Leave the bot.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    alias = message['from']['username']
    # remove from the list of users
    await queries.remove_user_by_uid(uid)
    message_remove_user = '@' + alias + ', your account was successfully removed.'
    return message_remove_user
