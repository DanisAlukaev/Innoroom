from misc import queries
from modules.users import auxiliary
import re


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



