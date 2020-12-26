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
               ', alias: ' + self.alias + \
               ', name: ' + self.name + \
               ', surname: ' + self.surname + ')'


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
    else:
        message = 'You are already in the list of users.'
        print(message)


def create_queue():
    # create new queue
    title = input()

    if title not in titles:
        queues[title] = Order(title=title)
    else:
        message = 'Queue with specified title is already exists'
        print(message)


def join_queue():
    # join to queue
    title = input()
    uid = input()

    users[uid].my_queues.append(title)
    if title in titles:
        queues[title].queue.append([uid, 0])
    else:
        message = 'Queue with specified title does not exist'
        print(message)


def quit_queue():
    # leave the queue
    title = input()
    uid = input()

    users[uid].my_queues.remove(title)
    for order in queues.items():
        key = order[0]
        for pair in order[1].queue:
            if pair[0] == uid:
                index = order[1].queue.index(pair)
                queues[key].queue.pop(index)

    if title in titles:
        for order in queues.items():
            key = order[0]
            for pair in order[1].queue:
                if pair[0] == uid:
                    index = order[1].queue.index(pair)
                    queues[title].queue.pop(index)
    else:
        message = 'Queue with specified title does not exist'
        print(message)


def remove_queue():
    # remove the queue
    title = input()

    if title in titles:
        queues.pop(title)
    else:
        message = 'Queue with specified title does not exist'
        print(message)


def remove_user():
    # delete the user
    uid = input()
    users.pop(uid)
    for order in queues.items():
        key = order[0]
        for pair in order[1].queue:
            if pair[0] == uid:
                index = order[1].queue.index(pair)
                queues[key].queue.pop(index)


def get_queues():
    # get all queues
    for queue in queues.values():
        print(queue.title)


def my_queues():
    # get my queues
    uid = input()
    print(users[uid].my_queues)


def current():
    # get current user in order
    title = input()
    print(queues[title].current)


def next():
    # get next user in order
    title = input()
    queues[title].current = (queues[title].current + 1) % len(queues[title].queue)


def skip():
    # skip one turn
    title = input()
    uid = input()

    for order in queues.items():
        key = order[0]
        for pair in order[1].queue:
            if pair[0] == uid:
                index = order[1].queue.index(pair)
                queues[title].queue[index][1] += 1


def state():
    # get current state of all queues
    for queue in queues.values():
        print(queue.title)
        for person in queue.queue:
            uid = person[0]
            name_uid = users[uid].name
            surname_uid = users[uid].surname

            if queue.current == queue.queue.index(person):
                print('> ' + name_uid + ' ' + surname_uid + ' : ' + str(person[1]))
            else:
                print(name_uid + ' ' + surname_uid + ' : ' + str(person[1]))


def give():
    # give money to person with specified alias
    # TODO: several people, all

    # who share money
    uid = input()
    # who take money
    alias = input()
    # amount of money
    money = int(input())

    if debts[uid][uid_dict[alias]] == 0:
        debts[uid_dict[alias]][uid] += money
    elif debts[uid][uid_dict[alias]] <= money:
        debts[uid_dict[alias]][uid] += money - debts[uid][uid_dict[alias]]
        debts[uid][uid_dict[alias]] = 0
    elif debts[uid][uid_dict[alias]] > money:
        debts[uid][uid_dict[alias]] -= money
        debts[uid_dict[alias]][uid] = 0


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
            if debt_key_2 == uid:
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
    share = money / number_users

    # TODO: send share to the give function


def update_user_dictionary():
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


# TODO: check presence of title and nicknames
# TODO: me/change info
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
        elif command == 'current':
            current()
        elif command == 'next':
            next()
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

        print(users, queues, debts)

        # read the command
        command = input()
