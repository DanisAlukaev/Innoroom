from users import users, alias_dict, uid_dict
import re


class Order:
    """
    Class describing the order.
    Contains queues that consist of pairs of user id and number of skips, current user.
    """

    def __init__(self, title: str):
        self.title = title
        self.queue = []
        self.current = 0

    def __repr__(self):
        return '(title: ' + self.title + \
               ', queue: ' + self.queue.__repr__() + \
               ', current: ' + str(self.current) + ')'


# user queues in format {title: order}
queues = {}


def leave(message):
    """
    Leave the bot.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']

    # remove from the list of users
    users.pop(uid)

    alias = alias_dict[uid]
    alias_dict.pop(uid)
    uid_dict.pop(alias)

    # remove user from each queue
    for title, details in queues.items():
        for user_pair in details.queue:
            if user_pair[0] == uid:
                # get index of user pair
                index = details.queue.index(user_pair)
                # remove user pair from list
                queues[title].queue.pop(index)
    message_remove_user = '@' + alias + ', your account was successfully removed.'
    return message_remove_user


def get_list_user_aliases():
    aliases = []
    for uid_user, detail_user in users.items():
        aliases.append(detail_user.alias)
    return aliases


def _check_presence_users(message):
    aliases = message['text'].replace('@', '').split(' ')[1:]
    # didn't pass verification
    fail_verification = []
    fail_verification_str = ''
    list_user_aliases = get_list_user_aliases()
    for alias_ in aliases:
        if alias_ not in list_user_aliases:
            fail_verification.append(alias_)
            fail_verification_str += '@' + alias_ + ' '
    return aliases, fail_verification, fail_verification_str


# TODO: check aliases
def remove_user(message):
    """
    Remove user of the bot.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    if re.fullmatch(r'/remove( @\w+)+', message['text'].replace('\n', '')):

        aliases, fail_verification, fail_verification_str = _check_presence_users(message)

        if len(fail_verification) == 0:
            message_remove_user = '@' + alias_dict[uid] + ', you have removed user(s)\n'
            for alias in aliases:
                uid_ = uid_dict[alias]

                # remove from the list of users
                users.pop(uid_)
                alias_dict.pop(uid_)
                uid_dict.pop(alias)

                # remove user from each queue
                for title, details in queues.items():
                    for user_pair in details.queue:
                        if user_pair[0] == uid_:
                            # get index of user pair
                            index = details.queue.index(user_pair)
                            # remove user pair from list
                            queues[title].queue.pop(index)
                message_remove_user += '• @' + alias + '.\n'
        else:
            message_remove_user = 'User with alias(es) ' + fail_verification_str + 'do(es) not registered in bot.'
    else:
        message_remove_user = 'Message does not match the required format. Check rules in /help.'
    return message_remove_user


def create_queue(message):
    """
    Create new queue.

    :param message: user's message.
    :return: reply.
    """

    if re.fullmatch(r'/create_queue \w+', message['text'].replace('\n', '')):
        # get information about the user
        title = message['text'].split(' ')[1]

        titles = queues.keys()
        if title not in titles:
            # create new queue
            queues[title] = Order(title=title)
            message_create_queue = 'Queue <b>' + title + '</b> was created.'
        else:
            message_create_queue = 'Queue with specified title is already exists.'
    else:
        message_create_queue = 'Message does not match the required format. Check rules in /help.'
    return message_create_queue


def join_queue(message):
    """
    Join to the queue.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    alias = message['from']['username']

    if re.fullmatch(r'/join_queue \w+', message['text'].replace('\n', '')):
        title = message['text'].split(' ')[1]
        titles = queues.keys()
        if uid not in users.keys():
            message_join_queue = '@' + alias + ', you are not a user of a bot.'
        elif title in titles:
            # check whether user is already in queue
            if title not in users[uid].my_queues:
                # set new tuple of id and initial number of skips
                queues[title].queue.append([uid, 0])
                # add queue to internal list of queues
                users[uid].my_queues.append(title)
                message_join_queue = '@' + alias + ', you are now in the queue <b>' + title + '</b>.'
            else:
                message_join_queue = '@' + alias + ', you are already in this queue.'
        else:
            message_join_queue = 'Queue with specified title does not exist.'
    else:
        message_join_queue = 'Message does not match the required format. Check rules in /help.'
    return message_join_queue


def quit_queue(message):
    """
    Quit from the queue.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    alias = message['from']['username']

    if re.fullmatch(r'/quit_queue \w+', message['text'].replace('\n', '')):
        title = message['text'].split(' ')[1]
        titles = queues.keys()
        if title in titles:
            # remove user from a list of queues
            for pair in queues[title].queue:
                if pair[0] == uid:
                    # get the index of user in the list
                    index = queues[title].queue.index(pair)
                    # remove user from the list
                    queues[title].queue.pop(index)
                    break
            # remove queue from user's internal data
            users[uid].my_queues.remove(title)
            if queues[title].current >= len(queues[title].queue):
                queues[title].current = 0
            message_quit_queue = '@' + alias + ', you are now out of the queue <b>' + title + '</b>.'
        else:
            message_quit_queue = 'Queue with specified title does not exist.'
    else:
        message_quit_queue = 'Message does not match the required format. Check rules in /help.'
    return message_quit_queue


def remove_queue(message):
    """
    Remove queue with a given title.

    :param message: user's message.
    :return: reply.
    """
    if re.fullmatch(r'/remove_queue \w+', message['text'].replace('\n', '')):
        # get information about the user
        title = message['text'].split(' ')[1]
        titles = queues.keys()
        if title in titles:
            # remove queue from list of queues
            queues.pop(title)
            # remove all entries of queue in users
            for user_id, user_details in users.items():
                if title in user_details.my_queues:
                    user_details.my_queues.pop(user_details.my_queues.index(title))
            message_remove_queue = 'Queue <b>' + title + '</b> was successfully removed.'
        else:
            message_remove_queue = 'Queue with specified title does not exist.'
    else:
        message_remove_queue = 'Message does not match the required format. Check rules in /help.'
    return message_remove_queue


def get_queues(message):
    """
    Get all queues in the bot.

    :param message: user's message.
    :return: reply.
    """
    # form a reply
    message_get_queues = ''
    for queue in queues.values():
        message_get_queues += '• ' + queue.title + '\n'
    if not message_get_queues:
        message_get_queues = 'There are no queues in bot.'
    else:
        message_get_queues = '<b>Available queues:</b>\n' + message_get_queues
    return message_get_queues


def my_queues(message):
    """
    Get queues of a sender.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']

    # form a reply
    message_my_queues = ''
    for queue_title in users[uid].my_queues:
        message_my_queues += '• ' + queue_title + '\n'
    if not message_my_queues:
        message_my_queues = '@' + alias_dict[uid] + ', you did not join any queue in bot.'
    else:
        message_my_queues = 'Queues of ' + users[uid].name + ':\n' + message_my_queues
    return message_my_queues


def current_user(message):
    """
    Get current user in a queue.

    :param message: user's message.
    :return: reply.
    """
    if re.fullmatch(r'/current_user \w+', message['text'].replace('\n', '')):
        # get information about the user
        title = message['text'].split(' ')[1]
        titles = queues.keys()
        if title in titles:
            if len(queues[title].queue) != 0:
                # get index of a current user in a queue in list
                index_current = queues[title].current
                # get id of a current user
                uid_current = queues[title].queue[index_current][0]
                message_current_user = '@' + alias_dict[uid_current] + ', it is now your turn in queue' + title + '.'
            else:
                message_current_user = 'Queue is empty.'
        else:
            message_current_user = 'Queue with specified title does not exist.'
    else:
        message_current_user = 'Message does not match the required format. Check rules in /help.'
    return message_current_user


def next_user(message):
    """
    Pass turn to the next user.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    alias = message['from']['username']

    if re.fullmatch(r'/next_user \w+', message['text'].replace('\n', '')):
        title = message['text'].split(' ')[1]
        titles = queues.keys()
        if title in titles:
            if len(queues[title].queue) != 0:
                # get current user in a queue
                current = queues[title].current
                # check whether user is current
                if queues[title].queue[current][0] == uid:
                    # check whether user had skipped turns
                    if queues[title].queue[current][1] == 0:
                        # pass turn to next user
                        queues[title].current = (queues[title].current + 1) % len(queues[title].queue)
                        current = queues[title].current
                        message_next_user = 'Turn went to @' + alias_dict[queues[title].queue[current][0]] + '.'
                    else:
                        # eliminate one skip
                        queues[title].queue[current][1] -= 1
                        message_next_user = '@' + alias + ', you have eliminated your skip.'
                else:
                    message_next_user = '@' + alias + ', it is not your turn.'
            else:
                message_next_user = 'Queue is empty.'
        else:
            message_next_user = 'Queue with specified title does not exist.'
    else:
        message_next_user = 'Message does not match the required format. Check rules in /help.'
    return message_next_user


def skip(message):
    """
    Skip the turn for a current user in a queue.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    alias = message['from']['username']
    if re.fullmatch(r'/skip \w+', message['text'].replace('\n', '')):
        title = message['text'].split(' ')[1]
        titles = queues.keys()
        if title in titles:
            if len(queues[title].queue) != 0:
                # get index of a current user in a queue in list
                current = queues[title].current
                # check whether user is current
                if queues[title].queue[current][0] == uid:
                    # increment skips' number of a current user
                    queues[title].queue[current][1] += 1
                    # pass turn to the next user
                    queues[title].current = (queues[title].current + 1) % len(queues[title].queue)
                    message_skip = '@' + alias + ', you have skipped your turn.'
                else:
                    message_skip = '@' + alias + ', now it is not your turn.'
            else:
                message_skip = 'Queue is empty.'
        else:
            message_skip = 'Queue with specified title does not exist.'
    else:
        message_skip = 'Message does not match the required format. Check rules in /help.'
    return message_skip


def get_states(message):
    """
    Get states of all queues.

    :param message: user's message.
    :return: reply.
    """
    # get current state of all queues
    message_state = ''
    # iterate through all queues
    for queue in queues.values():
        message_state += 'Queue <b>' + queue.title + '</b>.\n'
        # iterate through all users within the queue
        for person in queue.queue:
            uid = person[0]
            # get name
            name_uid = users[uid].name
            surname_uid = users[uid].surname
            # bold text for a current user
            if queue.current == queue.queue.index(person):
                message_state += '• <u>' + name_uid + ' ' + surname_uid + '</u> : ' + str(person[1]) + ' skips\n'
            else:
                message_state += '• ' + name_uid + ' ' + surname_uid + ' : ' + str(person[1]) + ' skips\n'
        message_state += '\n'
    return message_state
