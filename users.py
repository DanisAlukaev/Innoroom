import re


class User:
    """
    Class describing the user of a bot.
    Contains identification, name, surname, username, queues of a user.
    """

    def __init__(self, uid: int, alias: str, name: str, surname: str):
        self.uid = uid
        self.alias = alias
        self.name = name
        self.surname = surname
        self.my_queues = []

    def __str__(self):
        my_queues_string = ''
        for queue in self.my_queues:
            my_queues_string += queue + ' '
        return '<b>Profile account:</b>\n' + \
               'Alias: @' + self.alias + '\n' + \
               'Name: ' + self.name + '\n' + \
               'Surname: ' + self.surname + '\n' + \
               'Queues: ' + my_queues_string

    def __repr__(self):
        return '(uid:' + str(self.uid) + \
               ', Alias: @' + self.alias + \
               ', Name: ' + self.name + \
               ', Surname: ' + self.surname + \
               ', Queues: ' + self.my_queues.__repr__() + ')'


# list of users in format {uid: User}
users = {}
# pending requests
requests = {}
# dictionary to map alias to uid
alias_dict = {}
# dictionary to map uid to alias
uid_dict = {}


def request_join(message):
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

    if uid in users.keys():
        # sender is already in the list of users
        message_add_user = '@' + alias + ', you are already in the list of users.'
    elif uid in requests.keys():
        # sender has already sent request
        message_add_user = '@' + alias + ', your request has not been processed yet.'
    else:
        # create new user
        requests[uid] = User(uid=uid, alias=alias, name=name, surname=surname)
        # add alias and user id in auxiliary dictionary
        alias_dict[uid] = alias
        uid_dict[alias] = uid

        message_add_user = '@' + alias + ", your request was successfully sent.\n\n" + requests[uid].__str__()
    return message_add_user


def all_requests(message):
    """
    Return all requests to join.

    :param message: user's message.
    :return: reply.
    """
    message_all_requests = '<b>Current requests</b>\n'
    for requests_uid, requests_detail in requests.items():
        message_all_requests += '• @' + requests_detail.alias + '\n'
    return message_all_requests


def get_list_request_aliases():
    """
    Return all aliases of users in pending requests list.

    :return: reply.
    """
    aliases = []
    for uid_user, detail_user in requests.items():
        aliases.append(detail_user.alias)
    return aliases


def get_list_user_aliases():
    """
    Return all aliases of users in users list.

    :return: reply.
    """
    aliases = []
    for uid_user, detail_user in users.items():
        aliases.append(detail_user.alias)
    return aliases


def _check_presence_users(message):
    """
    Check whether all aliases specified by user are in requests list.

    :param message: user's message.
    :return: reply.
    """
    # get list of all aliases specified by user
    aliases = message['text'].replace('@', '').split(' ')[1:]
    # list of aliases of users that didn't send requests (and string consisting of them)
    fail_validation = []
    fail_validation_str = ''
    # list of aliases of users that sent requests
    list_request_aliases = get_list_request_aliases()
    for alias_ in aliases:
        if alias_ not in list_request_aliases:
            # alias is not present in requests list
            fail_validation.append(alias_)
            fail_validation_str += '@' + alias_ + ' '
    return aliases, fail_validation, fail_validation_str


def accept(message):
    """
    Accept request(s) to join of specified users.

    :param message: user's message.
    :return: reply.
    """
    # get alias of user
    alias = message['from']['username']

    if re.fullmatch(r'/accept( @\w+)+', message['text'].replace('\n', '')):
        # message is properly formatted

        # get parsed aliases and aliases that were failed to validate
        aliases, fail_validation, fail_validation_str = _check_presence_users(message)

        if len(fail_validation) == 0:
            # all aliases are in requests list
            message_accept = '@' + alias + ', you have added new user(s)\n'
            for alias in aliases:
                # copy sender information in users list
                users[uid_dict[alias]] = requests[uid_dict[alias]]
                # remove request
                requests.pop(uid_dict[alias])
                message_accept += '• @' + alias + '\n'
        else:
            # some aliases fail validation
            message_accept = 'User with alias(es) ' + fail_validation_str + "didn't send joining request in bot."
    else:
        # message fails to parse
        message_accept = 'Message does not match the required format. Check rules in /help.'
    return message_accept


def decline(message):
    """
    Decline request(s) to join of specified users.

    :param message: user's message.
    :return: reply.
    """
    # get alias of user
    alias = message['from']['username']

    if re.fullmatch(r'/decline( @\w+)+', message['text'].replace('\n', '')):
        # message is properly formatted

        # get parsed aliases and aliases that were failed to validate
        aliases, fail_validation, fail_validation_str = _check_presence_users(message)

        if len(fail_validation) == 0:
            # all aliases are in requests list
            message_decline = '@' + alias + ', you have declined request(s) of \n'
            for alias in aliases:
                # get id of user to remove
                uid_remove = uid_dict[alias]
                # remove entries for auxiliary dictionaries
                uid_dict.pop(alias)
                alias_dict.pop(uid_remove)
                # remove request
                requests.pop(uid_remove)
                message_decline += '• @' + alias + '\n'
        else:
            # some aliases fail validation
            message_decline = 'User with alias(es) ' + fail_validation_str + 'did not send joining request in bot.'
    else:
        # message fails to parse
        message_decline = 'Message does not match the required format. Check rules in /help.'
    return message_decline


def update_me(message):
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

    # update name, surname of user
    users[uid].name = name
    users[uid].surname = surname
    # get outdated alias
    previous_alias = users[uid].alias
    # update alias in users list
    users[uid].alias = alias
    # update alias in alias dictionary
    alias_dict[uid] = alias
    # remove outdated entry in uid dictionary
    uid_dict.pop(previous_alias)
    # update uid dictionary
    uid_dict[alias] = uid

    message_change_name = '@' + alias + ', your account was successfully updated.\n\n' + users[uid].__str__()
    return message_change_name
