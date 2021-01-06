from misc import queries
import re
import logging


# TODO: save the creator
async def create_queue(message):
    """
    Create new queue.

    :param message: user's message.
    :return: reply.
    """

    if re.fullmatch(r'/create_queue \w+', message['text'].replace('\n', '')):
        # message is properly formatted

        # get title of queue
        title = message['text'].split(' ')[1]

        queues = await queries.get_queues()
        titles = [queue['title'] for queue in queues]

        if title not in titles:
            # create new queue
            await queries.create_queue(title)
            message_create_queue = 'Queue <b>' + title + '</b> was created.'
        else:
            # there is no queue with given title
            message_create_queue = 'Queue with specified title is already exists.'
    else:
        # message fails to parse
        message_create_queue = 'Message does not match the required format. Check rules in /help.'
    return message_create_queue


async def join_queue(message):
    """
    Join to the queue.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    alias = message['from']['username']

    if re.fullmatch(r'/join_queue \w+', message['text'].replace('\n', '')):
        # message is properly formatted

        # get title of queue
        title = message['text'].split(' ')[1]

        queues = await queries.get_queues()
        titles = [queue['title'] for queue in queues]
        if title in titles:
            # queue with specified title exists
            user_titles = await queries.user_queues(uid)
            if title not in user_titles:
                # user is out of queue
                queue_id = (await queries.get_queue_id_by_title(title))[0]['id']
                user_id = (await queries.get_by_uid(uid))[0]['id']
                logging.info(user_id)
                await queries.join_queue(user_id, queue_id)
                message_join_queue = '@' + alias + ', you are now in the queue <b>' + title + '</b>.'
            else:
                # user is in queue
                message_join_queue = '@' + alias + ', you are already in this queue.'
        else:
            # there is no queue with given title
            message_join_queue = 'Queue with specified title does not exist.'
    else:
        # message fails to parse
        message_join_queue = 'Message does not match the required format. Check rules in /help.'
    return message_join_queue


async def remove_queue(message):
    """
    Remove queue with a given title.

    :param message: user's message.
    :return: reply.
    """
    if re.fullmatch(r'/remove_queue \w+', message['text'].replace('\n', '')):
        # message is properly formatted

        # get title of queue
        title = message['text'].split(' ')[1]

        queues = await queries.get_queues()
        titles = [queue['title'] for queue in queues]
        if title in titles:
            # queue with specified title exists

            # remove queue from list of queues
            await queries.remove_queue_by_title(title)
            message_remove_queue = 'Queue <b>' + title + '</b> was successfully removed.'
        else:
            # there is no queue with given title
            message_remove_queue = 'Queue with specified title does not exist.'
    else:
        # message fails to parse
        message_remove_queue = 'Message does not match the required format. Check rules in /help.'
    return message_remove_queue


async def get_queues(message):
    """
    Get all queues in the bot.

    :param message: user's message.
    :return: reply.
    """
    message_get_queues = ''
    queues = await queries.get_queues()
    titles = [queue['title'] for queue in queues]
    for title in titles:
        message_get_queues += '• ' + title + '\n'
    if not message_get_queues:
        message_get_queues = 'There are no queues in bot.'
    else:
        message_get_queues = '<b>Available queues:</b>\n' + message_get_queues
    return message_get_queues


async def my_queues(message):
    """
    Get queues of a sender.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    alias = message['from']['username']

    message_my_queues = ''
    queues = await queries.get_my_queues(uid)
    titles = [queue['title'] for queue in queues]

    for title in titles:
        message_my_queues += '• ' + title + '\n'
    if not message_my_queues:
        # there are no queues in built string
        message_my_queues = '@' + alias + ', you did not join any queue in bot.'
    else:
        message_my_queues = '<b>Your queues:</b>\n' + message_my_queues
    return message_my_queues
