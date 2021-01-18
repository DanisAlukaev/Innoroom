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

    user = await queries.get_user_by_uid(uid)
    if not user:
        return 'Send the request first.'

    # update alias, name, surname of user
    await queries.update_alias(alias, uid)
    await queries.update_name(name, uid)
    await queries.update_surname(surname, uid)
    message_change_name = '@' + alias + ', your account was successfully updated.\n\n' + (
        await auxiliary.user_data_to_string(uid))
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
    user_queues = await queries.get_my_queues(uid)
    # get all queues' titles
    user_titles = [queue['title'] for queue in user_queues]

    for title in user_titles:
        message_my_queues += '\n• ' + title

    message_my_queues = name + ', you did not join any queue in bot.' if not message_my_queues \
        else '<b>Your queues:</b>' + message_my_queues
    message_me += '\n\n' + message_my_queues

    # amount of money user owes
    total_debt = 0
    debts = await queries.get_debts(uid)
    credits = await queries.get_credits(uid)

    if not debts and credits:
        return 'Error.'

    # compute total debt of user
    for debt in debts:
        value_debt = int(debt['value'])
        if value_debt != 0:
            total_debt += value_debt
    message_me += '\n\n<b>Finances:</b>\nTotal debt: ' + str(total_debt) + '.\n'

    # amount of money shared with all users
    total_service = 0
    # compute total credit of user
    for credit in credits:
        value_credit = int(credit['value'])
        if value_credit != 0:
            total_service += value_credit
    message_me += 'Total service: ' + str(total_service) + '.'
    return message_me
