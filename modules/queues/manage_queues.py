from misc import queries
from modules.queues import auxiliary
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


# TODO: current user modify
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
            queues = await queries.user_queues(uid)
            user_titles = [queue['title'] for queue in queues]
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
    logging.info(titles)
    for title in titles:
        message_my_queues += '• ' + title + '\n'
    if not message_my_queues:
        # there are no queues in built string
        message_my_queues = '@' + alias + ', you did not join any queue in bot.'
    else:
        message_my_queues = '<b>Your queues:</b>\n' + message_my_queues
    return message_my_queues


async def get_states(message):
    """
    Get states of all queues.

    :param message: user's message.
    :return: reply.
    """
    message_state = ''
    queues = await queries.get_queues()

    if len(queues) == 0:
        message_state = 'There are no queues in bot.'
        return message_state

    for queue in queues:

        users_ordered = await auxiliary.get_users_in_queue_ordered(queue['title'])
        # go through all queues
        message_state += 'Queue <b>' + queue['title']
        if len(users_ordered) == 0:
            message_state += '</b> is empty.\n'
        else:
            message_state += ':</b>\n'
        for person in users_ordered:
            # get information about all users in queue

            current_user_index = queue['curr_user']

            skips = (await queries.get_skips_for_user(person['uid']))[0]['skips']

            if current_user_index == users_ordered.index(person):
                # underline text for a current user
                message_state += '• <u>' + person['name'] + ' ' + person['surname'] + '</u> : ' + str(
                    skips) + ' skips\n'
            else:
                message_state += '• ' + person['name'] + ' ' + person['surname'] + ' : ' + str(skips) + ' skips\n'
        message_state += '\n'
    return message_state


async def current_user(message):
    """
    Get current user in a queue.

    :param message: user's message.
    :return: reply.
    """
    if re.fullmatch(r'/current_user \w+', message['text'].replace('\n', '')):
        # message is properly formatted

        # get title of queue
        title = message['text'].split(' ')[1]

        queues = await queries.get_queues()
        titles = [queue['title'] for queue in queues]

        if title in titles:
            # queue with specified title exists
            users_ordered = await auxiliary.get_users_in_queue_ordered(title)
            if len(users_ordered) != 0:
                # queue is non-empty

                # get index of a current user in a queue in list
                current_index = await queries.get_current_user_index(title)
                # get id of a current user
                user = users_ordered[int(current_index)]
                message_current_user = '@' + user[
                    'alias'] + ', it is now your turn in queue <b>' + title + '</b>.'
            else:
                # there are no users in queue
                message_current_user = 'Queue is empty.'
        else:
            # there is no queue with given title
            message_current_user = 'Queue with specified title does not exist.'
    else:
        # message fails to parse
        message_current_user = 'Message does not match the required format. Check rules in /help.'
    return message_current_user


async def next_user(message):
    """
    Pass turn to the next user.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    alias = message['from']['username']

    if re.fullmatch(r'/next_user \w+', message['text'].replace('\n', '')):
        # message is properly formatted

        # get title of queue
        title = message['text'].split(' ')[1]

        queues = await queries.get_queues()
        titles = [queue['title'] for queue in queues]
        if title in titles:

            # queue with specified title exists
            users_ordered = await auxiliary.get_users_in_queue_ordered(title)

            if len(users_ordered) != 0:
                # queue is non-empty

                # get index of a current user in a queue in list
                current_index = await queries.get_current_user_index(title)
                # get id of a current user
                user = users_ordered[int(current_index)]

                if user['uid'] == uid:
                    # now it is turn of sender
                    skips = (await queries.get_skips_for_user(user['uid']))[0]['skips']
                    if skips == 0:
                        # user had not skipped turns

                        # pass turn to next user
                        current_index = (int(current_index) + 1) % len(users_ordered)
                        await queries.change_next_user(current_index, title)
                        message_next_user = 'Turn went to @' + users_ordered[current_index]['alias'] + '.'
                    else:
                        # eliminate one skip
                        skips -= 1
                        await queries.change_skips_for_user(skips, user['uid'])
                        message_next_user = '@' + alias + ', you have eliminated your skip.'
                else:
                    # now it is not turn of sender
                    message_next_user = '@' + alias + ', it is not your turn.'
            else:
                # there are no users in queue
                message_next_user = 'Queue is empty.'
        else:
            # there is no queue with given title
            message_next_user = 'Queue with specified title does not exist.'
    else:
        # message fails to parse
        message_next_user = 'Message does not match the required format. Check rules in /help.'
    return message_next_user


async def skip(message):
    """
    Skip the turn for a current user in a queue.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    alias = message['from']['username']

    if re.fullmatch(r'/skip \w+', message['text'].replace('\n', '')):
        # message is properly formatted

        # get title of queue
        title = message['text'].split(' ')[1]
        queues = await queries.get_queues()
        titles = [queue['title'] for queue in queues]
        if title in titles:
            # queue with specified title exists
            users_ordered = await auxiliary.get_users_in_queue_ordered(title)
            if len(users_ordered) != 0:
                # queue is non-empty

                # get index of a current user in a queue in list
                current_index = await queries.get_current_user_index(title)
                # get id of a current user
                user = users_ordered[int(current_index)]

                if user['uid'] == uid:
                    # now it is turn of sender

                    skips = (await queries.get_skips_for_user(user['uid']))[0]['skips']
                    skips += 1
                    await queries.change_skips_for_user(skips, user['uid'])
                    current_index = (int(current_index) + 1) % len(users_ordered)
                    await queries.change_next_user(current_index, title)
                    message_skip = '@' + alias + ', you have skipped your turn.'
                else:
                    # now it is not turn of sender
                    message_skip = '@' + alias + ', now it is not your turn.'
            else:
                # there are no users in queue
                message_skip = 'Queue is empty.'
        else:
            # there is no queue with given title
            message_skip = 'Queue with specified title does not exist.'
    else:
        # message fails to parse
        message_skip = 'Message does not match the required format. Check rules in /help.'
    return message_skip


async def quit_queue(message):
    """
    Quit from the queue.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    alias = message['from']['username']

    if re.fullmatch(r'/quit_queue \w+', message['text'].replace('\n', '')):
        # message is properly formatted

        # get title of queue
        title = message['text'].split(' ')[1]
        queues = await queries.get_queues()
        titles = [queue['title'] for queue in queues]
        if title in titles:
            # queue with specified title exists

            await queries.quit_queue(uid)
            users_ordered = await auxiliary.get_users_in_queue_ordered(title)
            current_index = await queries.get_current_user_index(title)
            if int(current_index) >= len(users_ordered):
                # handle index out of range situations
                await queries.change_next_user(0, title)

            message_quit_queue = '@' + alias + ', you are now out of the queue <b>' + title + '</b>.'
        else:
            # there is no queue with given title
            message_quit_queue = 'Queue with specified title does not exist.'
    else:
        # message fails to parse
        message_quit_queue = 'Message does not match the required format. Check rules in /help.'
    return message_quit_queue
