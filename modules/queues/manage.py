from misc import queries
from modules.queues import auxiliary
import re
import logging


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
        # access table queues
        queues = await queries.get_queues()
        # get queues' titles
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
        # access table queues
        queues = await queries.get_queues()
        # get queues' titles
        titles = [queue['title'] for queue in queues]

        if title in titles:
            # queue with specified title exists

            # get queues of user
            user_queues = await queries.get_my_queues(uid)
            # get titles of user queues
            user_titles = [queue['title'] for queue in user_queues]

            if title not in user_titles:
                # user is out of queue

                # get ordering before adding
                sorted_user_prev = await auxiliary.get_users_in_queue_ordered(title)

                logging.info(sorted_user_prev)

                # get id of queue in members table
                queue_id = (await queries.get_queue_id_by_title(title))['id']
                # get id of user in users in table
                user_id = (await queries.get_user_by_uid(uid))['id']
                # join queue
                await queries.join_queue(user_id, queue_id)

                # get index of a current user in a queue in list
                current_index = await queries.get_current_user_index(title)

                if sorted_user_prev:
                    # get id of a current user
                    curr_user = sorted_user_prev[current_index]
                    # get added user
                    user = await queries.get_user_by_uid(uid)
                    # get ordering after adding
                    sorted_user_after = await auxiliary.get_users_in_queue_ordered(title)

                    logging.info(sorted_user_after.index(user))
                    logging.info(sorted_user_after.index(curr_user))

                    if sorted_user_after.index(user) < sorted_user_after.index(curr_user):
                        logging.info('Here')
                        await queries.change_next_user(current_index + 1, title)

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
        # access table queues
        queues = await queries.get_queues()
        # get queues' titles
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
        # access table queues
        queues = await queries.get_queues()
        # get queues' titles
        titles = [queue['title'] for queue in queues]

        if title in titles:
            # queue with specified title exists

            # get queues of user
            user_queues = await queries.get_my_queues(uid)
            # get titles of user queues
            user_titles = [queue['title'] for queue in user_queues]

            if title in user_titles:

                # get ordered list of users in queues
                users_ordered = await auxiliary.get_users_in_queue_ordered(title)

                if len(users_ordered) != 0:
                    # queue is non-empty

                    # get index of a current user in a queue in list
                    current_index = await queries.get_current_user_index(title)
                    # get current user
                    user = users_ordered[int(current_index)]

                    if user['uid'] == uid:
                        # now it is turn of sender

                        # get number of skips
                        skips = await queries.get_skips_for_user(user['uid'], title)

                        if skips <= 0:
                            # user had not skipped turns

                            # pass turn to next user
                            current_index = (int(current_index) + 1) % len(users_ordered)
                            await queries.change_next_user(current_index, title)
                            message_next_user = 'Turn went to @' + users_ordered[current_index]['alias'] + '.'
                        else:
                            # eliminate one skip
                            skips -= 1
                            await queries.change_skips_for_user(skips, user['uid'], title)
                            message_next_user = '@' + alias + ', you have eliminated your skip.'
                    else:
                        # now it is not turn of sender
                        message_next_user = '@' + alias + ', it is not your turn.'
                else:
                    # there are no users in queue
                    message_next_user = 'Queue is empty.'
            else:
                message_next_user = '@' + alias + ', you are out of this queue.'
        else:
            # there is no queue with given title
            message_next_user = 'Queue with specified title does not exist.'
    else:
        # message fails to parse
        message_next_user = 'Message does not match the required format. Check rules in /help.'
    return message_next_user


async def add_progress(message):
    """
    Adds -1 to skip counter.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    alias = message['from']['username']

    if re.fullmatch(r'/add_progress \w+', message['text'].replace('\n', '')):
        # message is properly formatted

        # get title of queue
        title = message['text'].split(' ')[1]
        # access table queues
        queues = await queries.get_queues()
        # get queues' titles
        titles = [queue['title'] for queue in queues]

        if title in titles:
            # queue with specified title exists

            # get queues of user
            user_queues = await queries.get_my_queues(uid)
            # get titles of user queues
            user_titles = [queue['title'] for queue in user_queues]

            if title in user_titles:

                # get ordered list of users in queues
                users_ordered = await auxiliary.get_users_in_queue_ordered(title)

                if len(users_ordered) != 0:
                    # queue is non-empty

                    # get index of a current user in a queue in list
                    current_index = await queries.get_current_user_index(title)
                    # get current user
                    user = users_ordered[int(current_index)]

                    # get number of skips
                    skips = await queries.get_skips_for_user(user['uid'], title)
                    skips -= 1
                    await queries.change_skips_for_user(skips, user['uid'], title)
                    message_next_user = '@' + alias + ', you have added -1 to your skip counter.'
                    if skips < 0:
                        # pass turn to next user
                        current_index = (int(current_index) + 1) % len(users_ordered)
                        await queries.change_next_user(current_index, title)
                        message_next_user = 'Because your skip counter is below 0, turn went to @' + users_ordered[current_index]['alias'] + '.'
                else:
                    # there are no users in queue
                    message_next_user = 'Queue is empty.'
            else:
                message_next_user = '@' + alias + ', you are out of this queue.'
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
        # access table queues
        queues = await queries.get_queues()
        # get queues' titles
        titles = [queue['title'] for queue in queues]

        if title in titles:
            # queue with specified title exists

            # get queues of user
            user_queues = await queries.get_my_queues(uid)
            # get titles of user queues
            user_titles = [queue['title'] for queue in user_queues]

            if title in user_titles:

                # get ordered list of users in queues
                users_ordered = await auxiliary.get_users_in_queue_ordered(title)

                if len(users_ordered) != 0:
                    # queue is non-empty

                    # get index of a current user in a queue in list
                    current_index = await queries.get_current_user_index(title)
                    # get id of a current user
                    user = users_ordered[int(current_index)]

                    if user['uid'] == uid:
                        # now it is turn of sender

                        # get number of skips
                        skips = await queries.get_skips_for_user(user['uid'], title)
                        # increase number of skips
                        skips += 1
                        # update number of skips
                        await queries.change_skips_for_user(skips, user['uid'], title)
                        # update current index
                        current_index = (int(current_index) + 1) % len(users_ordered)
                        await queries.change_next_user(current_index, title)
                        message_skip = '@' + alias + ', you have skipped your turn.'
                    else:
                        # now it is not turn of sender
                        message_skip = '@' + alias + ', now it is not your turn.'
                else:
                    message_skip = '@' + alias + ', you are out of this queue.'
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
        # access table queues
        queues = await queries.get_queues()
        # get queues' titles
        titles = [queue['title'] for queue in queues]

        if title in titles:
            # queue with specified title exists

            # get queues of user
            user_queues = await queries.get_my_queues(uid)
            # get titles of user queues
            user_titles = [queue['title'] for queue in user_queues]

            if title in user_titles:
                # quit queue

                await queries.quit_queue(uid, title)
                # get ordered list of users in queues
                users_ordered = await auxiliary.get_users_in_queue_ordered(title)
                # get index of a current user in a queue in list
                current_index = await queries.get_current_user_index(title)

                if int(current_index) >= len(users_ordered):
                    # handle index out of range situations
                    await queries.change_next_user(0, title)

                message_quit_queue = '@' + alias + ', you are now out of the queue <b>' + title + '</b>.'
            else:
                message_quit_queue = '@' + alias + ', you are currently out of this queue.'
        else:
            # there is no queue with given title
            message_quit_queue = 'Queue with specified title does not exist.'
    else:
        # message fails to parse
        message_quit_queue = 'Message does not match the required format. Check rules in /help.'
    return message_quit_queue


async def remove_from_queue(message):
    """
    Remove user from the queue.

    :param message: user's message.
    :return: reply.
    """
    if re.fullmatch(r'/remove_from_queue @\w+ \w+', message['text'].replace('\n', '')):
        # message is properly formatted

        # get request
        request_message = message['text'].replace('@', '').split(' ')
        # get alias of user to be removed
        alias = request_message[1]
        # get user to be removed
        user = await queries.get_user_by_alias(alias)
        uid = user['uid']

        # get title of queue
        title = request_message[2]
        # access table queues
        queues = await queries.get_queues()
        # get queues' titles
        titles = [queue['title'] for queue in queues]

        if title in titles:
            # queue with specified title exists

            # get queues of user
            user_queues = await queries.get_my_queues(uid)
            # get titles of user queues
            user_titles = [queue['title'] for queue in user_queues]

            if title in user_titles:
                # quit queue

                await queries.quit_queue(uid, title)
                # get ordered list of users in queues
                users_ordered = await auxiliary.get_users_in_queue_ordered(title)
                # get index of a current user in a queue in list
                current_index = await queries.get_current_user_index(title)

                if int(current_index) >= len(users_ordered):
                    # handle index out of range situations
                    await queries.change_next_user(0, title)

                message_quit_queue = '@' + alias + ', you are now out of the queue <b>' + title + '</b>.'
            else:
                message_quit_queue = '@' + alias + ', you are currently out this queue.'
        else:
            # there is no queue with given title
            message_quit_queue = 'Queue with specified title does not exist.'
    else:
        # message fails to parse
        message_quit_queue = 'Message does not match the required format. Check rules in /help.'
    return message_quit_queue
