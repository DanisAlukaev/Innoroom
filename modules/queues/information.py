from misc import queries
from modules.queues import auxiliary
import re


async def get_queues(message):
    """
    Get all queues in the bot.

    :param message: user's message.
    :return: reply.
    """
    message_get_queues = ''
    # access table queues
    queues = await queries.get_queues()
    # get queues' titles
    titles = [queue['title'] for queue in queues]
    for title in titles:
        message_get_queues += '• ' + title + '\n'
    message_get_queues = 'There are no queues in bot.' if not message_get_queues \
        else '<b>Available queues:</b>\n' + message_get_queues
    return message_get_queues


async def my_queues(message):
    """
    Get queues of a sender.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    name = message['from']['first_name']

    message_my_queues = ''
    # access table queues
    queues = await queries.get_my_queues(uid)
    # get queues' titles
    titles = [queue['title'] for queue in queues]
    for title in titles:
        message_my_queues += '• ' + title + '\n'
    message_my_queues = name + ', you did not join any queue in bot.' if not message_my_queues \
        else name + ', your queues are:\n' + message_my_queues
    return message_my_queues


async def _state(queue):
    message_return = ''

    # get ordered list of users in queues
    users_ordered = await auxiliary.get_users_in_queue_ordered(queue['title'])

    message_return += 'Queue <b>' + queue['title']
    message_return += '</b> is empty.\n' if len(users_ordered) == 0 else ':</b>\n'

    for user in users_ordered:
        # get information about all users in queue

        # get index of current user
        current_user_index = queue['curr_user']
        # get number of skips
        skips = await queries.get_skips_for_user(user['uid'], queue['title'])

        if current_user_index == users_ordered.index(user):
            # underline text for a current user
            message_return += '• <u>' + user['name'] + ' ' + user['surname'] + '</u> : ' + str(
                skips) + ' skips\n'
        else:
            message_return += '• ' + user['name'] + ' ' + user['surname'] + ' : ' + str(skips) + ' skips\n'
    message_return += '\n'
    return message_return


async def get_state(message):
    """
    Get states of all queues.

    :param message: user's message.
    :return: reply.
    """
    if not re.fullmatch(r'/get_state \w+', message['text'].replace('\n', '')):
        # message fails to parse
        return 'Message does not match the required format. Check rules in /help.'

    # get title of queue
    title = message['text'].split(' ')[1]
    # access table queues
    queues = await queries.get_queues()
    # get queues' titles
    titles = [queue['title'] for queue in queues]

    if title not in titles:
        # there is no queue with given title
        return 'Queue with specified title does not exist.'

    # queue with specified title exists
    queue = await queries.get_queue_by_title(title)
    if not queue:
        return 'Error.'
    message_state = await _state(queue)
    return message_state


async def get_states(message):
    """
    Get states of all queues.

    :param message: user's message.
    :return: reply.
    """
    message_state = ''
    # access table queues
    queues = await queries.get_queues()

    if len(queues) == 0:
        return 'There are no queues in bot.'

    # generate message
    for queue in queues:
        message_state += await _state(queue)
    return message_state


async def current_user(message):
    """
    Get current user in a queue.

    :param message: user's message.
    :return: reply.
    """
    if not re.fullmatch(r'/current_user \w+', message['text'].replace('\n', '')):
        # message fails to parse
        message_current_user = 'Message does not match the required format. Check rules in /help.'

    # get title of queue
    title = message['text'].split(' ')[1]
    # access table queues
    queues = await queries.get_queues()
    # get queues' titles
    titles = [queue['title'] for queue in queues]

    if title not in titles:
        # there is no queue with given title
        return 'Queue with specified title does not exist.'

    # get ordered list of users in queues
    users_ordered = await auxiliary.get_users_in_queue_ordered(title)

    if len(users_ordered) == 0:
        # there are no users in queue
        return 'Queue is empty.'

    # get index of a current user in a queue in list
    current_index = await queries.get_current_user_index(title)
    # get id of a current user
    user = users_ordered[int(current_index)]
    message_current_user = '@' + user['alias'] + ', it is now your turn in queue <b>' + title + '</b>.'
    return message_current_user
