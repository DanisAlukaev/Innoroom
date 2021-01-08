from misc import queries
from modules.users import auxiliary


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
        message_add_user = name + ', you are already in the list of users.'
    elif uid in (await auxiliary.get_request_ids()):
        # sender has already sent request
        message_add_user = name + ', your request has not been processed yet.'
    else:
        # create new request
        await queries.add_request(uid, alias, name, surname)
        # new request was created
        profile = await auxiliary.user_data_to_string(uid)
        message_add_user = name + ", your request was successfully sent.\n\n" + profile
    return message_add_user


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
