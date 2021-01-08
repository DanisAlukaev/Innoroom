from misc import queries
from modules.users import auxiliary


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

    if len(await queries.get_user_by_uid(uid)) != 0:
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


async def me(message):
    """
    Display information about the user.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    name = message['from']['first_name']

    message_my_queues = ''
    # get serialized profile
    message_me = await auxiliary.user_data_to_string(uid)
    # get user queues
    queues = await queries.get_my_queues(uid)
    # get all queues' titles
    titles = [queue['title'] for queue in queues]

    for title in titles:
        message_my_queues += '\n• ' + title
    if not message_my_queues:
        # there are no queues in built string
        message_my_queues = name + ', you did not join any queue in bot.'
    else:
        message_my_queues = '<b>Your queues:</b>' + message_my_queues
    message_me += '\n\n' + message_my_queues

    # amount of money user owes
    total_debt = 0
    debts = await queries.get_debts(uid)
    # compute total debt of user
    for debt in debts:
        value_debt = int(debt['value'])
        if value_debt != 0:
            total_debt += value_debt
    message_me += '\n\n<b>Finances:</b>\nTotal debt: ' + str(total_debt) + '.\n'

    # amount of money shared with all users
    total_service = 0
    credits = await queries.get_credits(uid)
    # compute total credit of user
    for credit in credits:
        value_credit = int(credit['value'])
        if value_credit != 0:
            total_service += value_credit
    message_me += 'Total service: ' + str(total_service) + '.'
    return message_me
