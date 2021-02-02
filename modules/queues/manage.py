from misc import queries
from modules.queues import auxiliary
import re


async def create_queue(message):
    """
    Create new queue.

    :param message: user's message.
    :return: reply.
    """
    if not re.fullmatch(r'/create_queue( \w+)+', message['text'].replace('\n', '')):
        # message fails to parse
        return 'Message does not match the required format. Check rules in /help.'

    # get parsed titles and aliases that were failed to validate
    titles = message['text'].split(' ')[1:]
    titles, fail_validation, fail_validation_str = await auxiliary.check_absence_queues(titles)

    if len(fail_validation) != 0:
        # there is no queue with given title
        return 'Queue(s) ' + fail_validation_str + 'is/are already exist(s).'

    created_queues = ''
    for title_ in titles:
        # create new queue
        await queries.create_queue(title_)
        created_queues += title_ + ' '
    message_create_queue = 'Queue(s) <b>' + created_queues + '</b>was/were created.'
    return message_create_queue


async def join_queue(message):
    """
    Join to the queue.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    name = message['from']['first_name']

    if not re.fullmatch(r'/join_queue( \w+)+', message['text'].replace('\n', '')):
        # message fails to parse
        return 'Message does not match the required format. Check rules in /help.'

    # message is properly formatted

    # get parsed titles and aliases that were failed to validate
    titles = message['text'].split(' ')[1:]
    titles, fail_validation, fail_validation_str = await auxiliary.check_presence_queues(titles)

    if len(fail_validation) != 0:
        # there is no queue with given title
        return 'Queue(s) ' + fail_validation_str + 'do(es) not exist.'

    titles, fail_validation, fail_validation_str = await auxiliary.check_presence_for_user(titles, uid)

    if len(fail_validation) != 0:
        # user is in queue
        return name + ', you are already in queue(s) ' + fail_validation_str

    added_queues = ''
    for title in titles:
        # get ordering before adding
        sorted_user_prev = await auxiliary.get_users_in_queue_ordered(title)

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

            if sorted_user_after.index(user) < sorted_user_after.index(curr_user):
                # handle out of range situation
                await queries.change_next_user(current_index + 1, title)
        added_queues += title + ' '
    message_join_queue = name + ', you are now in the queue(s) <b>' + added_queues + '</b>'
    return message_join_queue


async def remove_queue(message):
    """
    Remove queue with a given title.

    :param message: user's message.
    :return: reply.
    """
    if not re.fullmatch(r'/remove_queue \w+', message['text'].replace('\n', '')):
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

    # remove queue from list of queues
    await queries.remove_queue_by_title(title)
    message_remove_queue = 'Queue <b>' + title + '</b> was successfully removed.'
    return message_remove_queue


async def next_user(message):
    """
    Pass turn to the next user.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    name = message['from']['first_name']

    if not re.fullmatch(r'/next_user \w+', message['text'].replace('\n', '')):
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

    # get queues of user
    user_queues = await queries.get_my_queues(uid)
    # get titles of user queues
    user_titles = [queue['title'] for queue in user_queues]

    if title not in user_titles:
        # user is out of this queue
        return name + ', you are out of this queue.'

    # get ordered list of users in queues
    users_ordered = await auxiliary.get_users_in_queue_ordered(title)

    if len(users_ordered) == 0:
        # there are no users in queue
        return 'Queue is empty.'

    # get index of a current user in a queue in list
    current_index = await queries.get_current_user_index(title)
    # get current user
    user = users_ordered[int(current_index)]

    if user['uid'] != uid:
        # now it is not turn of sender
        return name + ', it is not your turn.'

    # get number of skips
    skips = await queries.get_skips_for_user(user['uid'], title)

    if skips <= 0:
        # user has no skipped turns

        # pass turn to next user
        current_index = (int(current_index) + 1) % len(users_ordered)
        await queries.change_next_user(current_index, title)
        message_next_user = 'Turn in the queue ' + title + \
                            ' went to @' + users_ordered[current_index]['alias'] + '.'
    else:
        # eliminate one skip
        skips -= 1
        await queries.change_skips_for_user(skips, user['uid'], title)
        message_next_user = name + ', you have eliminated your skip.'
    return message_next_user


async def add_progress(message):
    """
    Adds -1 to skip counter.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    name = message['from']['first_name']

    if not re.fullmatch(r'/add_progress \w+', message['text'].replace('\n', '')):
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

    # get queues of user
    user_queues = await queries.get_my_queues(uid)
    # get titles of user queues
    user_titles = [queue['title'] for queue in user_queues]

    if title not in user_titles:
        # user is out of this queue
        return name + ', you are out of this queue.'

    # get ordered list of users in queues
    users_ordered = await auxiliary.get_users_in_queue_ordered(title)

    if len(users_ordered) == 0:
        # there are no users in queue
        return 'Queue is empty.'

    # get number of skips
    skips = await queries.get_skips_for_user(uid, title)
    skips -= 1
    await queries.change_skips_for_user(skips, uid, title)
    message_next_user = name + ', you have added -1 to your skip counter.'
    return message_next_user


async def skip(message):
    """
    Skip the turn for a current user in a queue.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    name = message['from']['first_name']

    if not re.fullmatch(r'/skip \w+', message['text'].replace('\n', '')):
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
        message_skip = 'Queue with specified title does not exist.'

    # get queues of user
    user_queues = await queries.get_my_queues(uid)
    # get titles of user queues
    user_titles = [queue['title'] for queue in user_queues]

    if title not in user_titles:
        # there are no users in queue
        return 'Queue is empty.'

    # get ordered list of users in queues
    users_ordered = await auxiliary.get_users_in_queue_ordered(title)

    if len(users_ordered) == 0:
        # there are no users in queue
        return 'Queue is empty.'

    # get index of a current user in a queue in list
    current_index = await queries.get_current_user_index(title)
    # get id of a current user
    user = users_ordered[int(current_index)]

    if user['uid'] != uid:
        # now it is not turn of sender
        return name + ', now it is not your turn.'

    # get number of skips
    skips = await queries.get_skips_for_user(user['uid'], title)
    # increase number of skips
    skips += 1
    # update number of skips
    await queries.change_skips_for_user(skips, user['uid'], title)
    # update current index
    current_index = (int(current_index) + 1) % len(users_ordered)
    await queries.change_next_user(current_index, title)
    message_skip = name + ', you have skipped your turn.'
    return message_skip


async def set_current(message):
    """
    Skip the turn for a current user in a queue.

    :param message: user's message.
    :return: reply.
    """

    if not re.fullmatch(r'/set_current \w+ @\w+', message['text'].replace('\n', '')):
        # message fails to parse
        return 'Message does not match the required format. Check rules in /help.'

    parsed_message = message['text'].replace('\n', '').replace('@', '').split(' ')
    # get title of queue
    title = parsed_message[1]
    # get alias of specified user
    alias = parsed_message[2]

    # access table queues
    queues = await queries.get_queues()
    # get queues' titles
    titles = [queue['title'] for queue in queues]

    if title not in titles:
        # there is no queue with given title
        return 'Queue with specified title does not exist.'

    user_ = await queries.get_user_by_alias(alias)
    # get queues of user
    user_queues = await queries.get_my_queues(user_['uid'])
    # get titles of user queues
    user_titles = [queue['title'] for queue in user_queues]

    if title not in user_titles:
        # user is out of the specified queue
        return '@' + alias + ' is out of the queue <b>' + title + '</b>.'

    # get ordered list of users in queues
    users_ordered = await auxiliary.get_users_in_queue_ordered(title)

    if len(users_ordered) == 0:
        # there are no users in queue
        return 'Queue is empty.'

    # get index of specified user
    current_index = users_ordered.index(user_)
    # set current index to user
    await queries.change_next_user(current_index, title)
    message_set = 'Turn in the queue <b>' + title + '</b> went to @' + alias + '.'
    return message_set


async def quit_queue(message):
    """
    Quit from the queue.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    name = message['from']['first_name']

    if not re.fullmatch(r'/quit_queue \w+', message['text'].replace('\n', '')):
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

    # get queues of user
    user_queues = await queries.get_my_queues(uid)
    # get titles of user queues
    user_titles = [queue['title'] for queue in user_queues]

    if title not in user_titles:
        # user is out of specified queue
        return name + ', you are currently out of this queue.'

    # quit queue
    await queries.quit_queue(uid, title)
    # get ordered list of users in queues
    users_ordered = await auxiliary.get_users_in_queue_ordered(title)
    # get index of a current user in a queue in list
    current_index = await queries.get_current_user_index(title)

    if int(current_index) >= len(users_ordered):
        # handle index out of range situations
        await queries.change_next_user(0, title)
    message_quit_queue = name + ', you are now out of the queue <b>' + title + '</b>.'
    return message_quit_queue


async def remove_from_queue(message):
    """
    Remove user from the queue.

    :param message: user's message.
    :return: reply.
    """
    if not re.fullmatch(r'/remove_from_queue @\w+ \w+', message['text'].replace('\n', '')):
        # message fails to parse
        return 'Message does not match the required format. Check rules in /help.'

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

    if title not in titles:
        # there is no queue with given title
        return 'Queue with specified title does not exist.'

    # get queues of user
    user_queues = await queries.get_my_queues(uid)
    # get titles of user queues
    user_titles = [queue['title'] for queue in user_queues]

    if title not in user_titles:
        return '@' + alias + ', you are currently out this queue.'

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
    return message_quit_queue
