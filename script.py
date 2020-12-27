class User:
    """
    Class describing the user of a bot.
    Contains Name, Surname of a user.
    """

    def __init__(self, uid, alias, name, surname):
        self.uid = uid
        self.alias = alias
        self.name = name
        self.surname = surname
        self.my_queues = []

    def __repr__(self):
        return '(uid:' + self.uid + \
               ', alias: @' + self.alias + \
               ', name: ' + self.name + \
               ', surname: ' + self.surname + \
               ', queues: ' + self.my_queues.__repr__() + ')'


class Order:
    """
    Class describing the order.
    Contains queues that consist of pairs of user id and number of skips, current user.
    """

    def __init__(self, title):
        self.title = title
        self.queue = []
        self.current = 0

    def __repr__(self):
        return '(title: ' + self.title + \
               ', queue: ' + self.queue.__repr__() + \
               ', current: ' + str(self.current) + ')'


# list of users in format {uid: User}
users = {}
# user queues in format {title: order}
queues = {}
# users' debts
debts = {}
# dictionary to map alias to uid
alias_dict = {}
# dictionary to map uid to alias
uid_dict = {}


def add_user():
    # add user to the list
    uid = input()
    alias = input()
    name = input()
    surname = input()

    if uid not in uids:
        users[uid] = User(uid=uid, alias=alias, name=name, surname=surname)
        alias_dict[uid] = alias
        uid_dict[alias] = uid
        message_add_user = 'You were successfully added to the list of users.'
    else:
        message_add_user = 'You are already in the list of users.'
    print(message_add_user)


def me():
    # display information about the user
    uid = input()
    message_me = users[uid]
    print(message_me)


def change_alias():
    # change alias of the user
    uid = input()
    alias = input()
    previous_alias = users[uid].alias
    users[uid].alias = alias

    uid_temp = ''
    for uid_alias, alias_alias in alias_dict.items():
        if alias_alias == previous_alias:
            uid_temp = uid_alias
    alias_dict[uid_temp] = alias

    uid_dict[alias] = uid_dict[previous_alias]
    uid_dict.pop(previous_alias)

    message_change_alias = 'Your alias was changed to ' + alias + '.'
    print(message_change_alias)


def change_name():
    # change name of the user
    uid = input()
    name = input()
    users[uid].name = name
    message_change_name = 'Your name was changed to ' + name + '.'
    print(message_change_name)


def change_surname():
    # change surname of the user
    uid = input()
    surname = input()
    users[uid].surname = surname
    message_change_surname = 'Your surname was changed to ' + surname + '.'
    print(message_change_surname)


def create_queue():
    # create new queue
    title = input()

    if title not in titles:
        queues[title] = Order(title=title)
        message_create_queue = 'Queue ' + title + ' was created.'
    else:
        message_create_queue = 'Queue with specified title is already exists.'
    print(message_create_queue)


def join_queue():
    # join to queue
    title = input()
    uid = input()

    if title in titles:
        if title not in users[uid].my_queues:
            queues[title].queue.append([uid, 0])
            users[uid].my_queues.append(title)
            message_join_queue = 'You are now in the queue ' + title + '.'
        else:
            message_join_queue = 'You are already in this queue.'
    else:
        message_join_queue = 'Queue with specified title does not exist.'
    print(message_join_queue)


def quit_queue():
    # leave the queue
    title = input()
    uid = input()

    if title in titles:
        for pair in queues[title].queue:
            if pair[0] == uid:
                index = queues[title].queue.index(pair)
                queues[title].queue.pop(index)
                break
        users[uid].my_queues.remove(title)
        message_quit_queue = 'You are now out of queue ' + title + '.'
    else:
        message_quit_queue = 'Queue with specified title does not exist.'
    print(message_quit_queue)


def remove_queue():
    # remove the queue
    title = input()

    if title in titles:
        queues.pop(title)
        for user_id, user_details in users.items():
            if title in user_details.my_queues:
                user_details.my_queues.pop(user_details.my_queues.index(title))
        message_remove_queue = 'Queue ' + title + ' was successfully removed.'
    else:
        message_remove_queue = 'Queue with specified title does not exist.'
    print(message_remove_queue)


def remove_user():
    # delete the user
    uid = input()

    users.pop(uid)
    alias = alias_dict[uid]
    alias_dict.pop(uid)
    uid_dict.pop(alias)

    for order in queues.items():
        key = order[0]
        for pair in order[1].queue:
            if pair[0] == uid:
                index = order[1].queue.index(pair)
                queues[key].queue.pop(index)
    message_remove_user = 'Your account was successfully removed.'
    print(message_remove_user)


def get_queues():
    # get all queues
    message_get_queues = ''
    for queue in queues.values():
        message_get_queues += queue.title + '\n'
    print(message_get_queues)


def my_queues():
    # get my queues
    uid = input()
    message_my_queues = ''
    for queue_title in users[uid].my_queues:
        message_my_queues += queue_title + '\n'
    print(message_my_queues)


def current_user():
    # get current user in order
    title = input()

    if title in titles:
        index_current = queues[title].current
        uid_current = queues[title].queue[index_current][0]
        message_current_user = alias_dict[uid_current]
    else:
        message_current_user = 'Queue with specified title does not exist.'
    print(message_current_user)


def next_user():
    # get next user in order
    uid = input()
    title = input()

    if title in titles:
        current = queues[title].current
        if queues[title].queue[current][0] == uid:
            if queues[title].queue[current][1] == 0:
                queues[title].current = (queues[title].current + 1) % len(queues[title].queue)
                current = queues[title].current
                message_next_user = 'Turn went to ' + alias_dict[queues[title].queue[current][0]] + '.'
            else:
                queues[title].queue[current][1] -= 1
                message_next_user = 'You have eliminated your skip.'
        else:
            message_next_user = 'It is not your turn.'
    else:
        message_next_user = 'Queue with specified title does not exist.'
    print(message_next_user)


def skip():
    # skip one turn
    title = input()
    uid = input()

    current = queues[title].current
    if title not in titles:
        message_skip = 'Queue with specified title does not exist.'
    elif queues[title].queue[current][0] == uid:
        queues[title].queue[current][1] += 1
        queues[title].current = (queues[title].current + 1) % len(queues[title].queue)
        message_skip = 'You have skipped your turn.'
    else:
        message_skip = 'Now it is not your turn.'
    print(message_skip)


def state():
    # get current state of all queues
    message_state = ''
    for queue in queues.values():
        message_state += queue.title + '\n'
        for person in queue.queue:
            uid = person[0]
            name_uid = users[uid].name
            surname_uid = users[uid].surname

            if queue.current == queue.queue.index(person):
                message_state += '> ' + name_uid + ' ' + surname_uid + ' : ' + str(person[1]) + '\n'
            else:
                message_state += '  ' + name_uid + ' ' + surname_uid + ' : ' + str(person[1]) + '\n'
    print(message_state)


def give():
    # give money to person with specified alias

    # who share money
    uid = input()
    # who take money
    aliases = input().replace(' ', '').split(',')
    # amount of money
    money = int(input())

    share_give = money / len(aliases)
    for alias in aliases:
        change_debts_dictionary(uid=uid, alias=alias, money=share_give)


def change_debts_dictionary(uid, alias, money):
    # update debts dictionary
    if alias in uid_dict.keys():
        if debts[uid][uid_dict[alias]] == 0:
            debts[uid_dict[alias]][uid] += money
        elif debts[uid][uid_dict[alias]] <= money:
            debts[uid_dict[alias]][uid] += money - debts[uid][uid_dict[alias]]
            debts[uid][uid_dict[alias]] = 0
        elif debts[uid][uid_dict[alias]] > money:
            debts[uid][uid_dict[alias]] -= money
            debts[uid_dict[alias]][uid] = 0
        message_change_debts = 'You have gave ' + str(money) + ' to @' + alias + '.\n'
    else:
        message_change_debts = 'There is no user with alias @' + alias
    print(message_change_debts)


def get_my_debts():
    # get list of debts to other users

    # id of a user
    uid = input()

    message_details = 'Your debt to the\n'
    total = 0
    for key, value in debts[uid].items():
        total += value
        if value != 0:
            message_details += users[key].name + ' ' + users[key].surname + ' is ' + str(value) + '\n'
    message_total = 'Your debt in total is ' + str(total) + '.\n'
    print(message_total)
    if total != 0:
        print(message_details)


def get_my_services():
    # get list of services to the other users

    # id of a user
    uid = input()

    total = 0
    message_details = 'Your service for the\n'
    for debt_key_1, debt_value_1 in debts.items():
        for debt_key_2, debt_value_2 in debt_value_1.items():
            if debt_key_2 == uid and debt_value_2 != 0:
                total += debt_value_2
                message_details += users[debt_key_1].name + ' ' + users[debt_key_1].surname + ' is ' + str(
                    debt_value_2) + '\n'
    message_total = 'Your service in total is ' + str(total) + '.\n'
    print(message_total)
    if total != 0:
        print(message_details)


def share():
    # share money with all users

    # id of a user
    uid = input()
    # amount of money
    money = int(input())

    # number of users
    number_users = len(users)
    # share for each user
    share_money = money / (number_users - 1)

    # update debts dictionary for all users
    for user_uid, user_details in users.items():
        if user_uid != uid:
            alias = user_details.alias
            change_debts_dictionary(uid=uid, alias=alias, money=share_money)


def update_user_dictionary():
    # auxiliary
    # update dictionary with debts
    for cur_uid_1 in uids:
        if cur_uid_1 in debts:
            arrears = debts[cur_uid_1]
        else:
            arrears = {}
        for cur_uid_2 in uids:
            if cur_uid_2 not in arrears and cur_uid_2 != cur_uid_1:
                arrears[cur_uid_2] = 0
        debts[cur_uid_1] = arrears

    debt_delete_outer = ''
    for debtor, people in debts.items():
        if debtor not in uids:
            debt_delete_outer = debtor
        debt_delete_inner = ''
        for person_uid, value_debt in people.items():
            if person_uid not in uids:
                debt_delete_inner = person_uid
        if debt_delete_inner:
            people.pop(debt_delete_inner)
    if debt_delete_outer:
        debts.pop(debt_delete_outer)


# TODO: check functionality
# TODO: fix messages
if __name__ == "__main__":
    # read the command
    command = input()
    # continuously read the prompt
    while command != 'exit':
        # get all user ids
        uids = users.keys()
        # get all titles
        titles = queues.keys()

        # run the command
        if command == 'add_user':
            add_user()
        elif command == 'me':
            me()
        elif command == 'change_alias':
            change_alias()
        elif command == 'change_name':
            change_name()
        elif command == 'change_surname':
            change_surname()
        elif command == 'create_queue':
            create_queue()
        elif command == 'join_queue':
            join_queue()
        elif command == 'quit_queue':
            quit_queue()
        elif command == 'remove_queue':
            remove_queue()
        elif command == 'remove_user':
            remove_user()
        elif command == 'get_queues':
            get_queues()
        elif command == 'my_queues':
            my_queues()
        elif command == 'current_user':
            current_user()
        elif command == 'next_user':
            next_user()
        elif command == 'skip':
            skip()
        elif command == 'state':
            state()
        elif command == 'give':
            give()
        elif command == 'my_debts':
            get_my_debts()
        elif command == 'my_services':
            get_my_services()
        elif command == 'share':
            share()
        else:
            # there is no such command
            message = 'Wrong command'
            print(message)
        update_user_dictionary()

        # for debugging
        print(users, queues, debts, alias_dict, uid_dict, sep='\n')

        # read the command
        command = input()
