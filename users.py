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
# dictionary to map alias to uid
alias_dict = {}
# dictionary to map uid to alias
uid_dict = {}


def register(message):
    """
    Register user in the bot, i.e. save information about the user.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    alias = message['from']['username']
    name = message['from']['first_name']
    surname = message['from']['last_name']

    # check whether user is already in the list of users
    if uid not in users.keys():
        # create new user
        users[uid] = User(uid=uid, alias=alias, name=name, surname=surname)
        # TODO: remove
        alias_dict[uid] = alias
        uid_dict[alias] = uid
        # inform that the user was registered
        message_add_user = '@' + alias + ', you were successfully added to the list of users.\n\n' + users[
            uid].__str__()
    else:
        message_add_user = '@' + alias + ', you are already in the list of users.'
    print(users, uid_dict, alias_dict)
    return message_add_user


def me(message):
    # display information about the user
    uid = message['from']['id']
    message_me = users[uid].__str__()
    return message_me


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

    # update information about the user
    users[uid].name = name
    users[uid].surname = surname
    # TODO: remove previous alias
    previous_alias = users[uid].alias
    users[uid].alias = alias
    uid_temp = ''
    for uid_alias, alias_alias in alias_dict.items():
        if alias_alias == previous_alias:
            uid_temp = uid_alias
    alias_dict[uid_temp] = alias
    uid_temp = uid_dict[previous_alias]
    uid_dict.pop(previous_alias)
    uid_dict[alias] = uid_temp

    # display message
    print(users, alias_dict, uid_dict, sep='\n')
    message_change_name = '@' + alias + ', your account was successfully updated.\n\n' + users[uid].__str__()
    return message_change_name
