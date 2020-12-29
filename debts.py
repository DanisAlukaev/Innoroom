from users import users, alias_dict, uid_dict

# users' debts
debts = {}


# TODO: include in share only aliases that are registered -> _change_debts_dictionary
# TODO: concatenate all responses from _change_debts_dictionary
# TODO: validator
def give(message):
    """
    Give debt for specified users.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    alias = message['from']['username']

    money = int(message['text'].split(' ')[1])
    aliases = message['text'].split(' ')[2:]

    share_give = money / len(aliases)
    aliases_str = ''

    for alias in aliases:
        aliases_str += '@' + alias + ' '
        # update debt list
        _change_debts_dictionary(uid=uid, alias=alias, money=share_give)
    message_give = '@' + alias + ', you have given ' + str(money) + ' to ' + aliases_str
    return message_give


# TODO: awake after all method's calls
def _change_debts_dictionary(uid, alias, money):
    """
    Update debts dictionary.

    :param uid: id of a creditor.
    :param alias: alias of a debtor.
    :param money: credit.
    :return reply
    """
    # check whether user with a given alias does exist
    if alias in uid_dict.keys():
        # check whether debt of a creditor is 0
        if debts[uid][uid_dict[alias]] == 0:
            debts[uid_dict[alias]][uid] += money
        # debt of a creditor is less than a given credit
        elif debts[uid][uid_dict[alias]] <= money:
            debts[uid_dict[alias]][uid] += money - debts[uid][uid_dict[alias]]
            debts[uid][uid_dict[alias]] = 0
        # debt of a creditor is greater than a given credit
        elif debts[uid][uid_dict[alias]] > money:
            debts[uid][uid_dict[alias]] -= money
            debts[uid_dict[alias]][uid] = 0
        message_change_debts = 'You have gave ' + str(money) + ' to @' + alias + '.\n'
    else:
        message_change_debts = 'There is no user with alias @' + alias
    return message_change_debts


def get_my_debts(message):
    """
    Get all debts of a user.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']

    message_details = 'Your debt to the\n'
    total_debts = 0
    for creditor, value in debts[uid].items():
        if value != 0:
            # increase value of a total debt
            total_debts += value
            message_details += users[creditor].name + ' ' + users[creditor].surname + ' is ' + str(value) + '\n'
    message_total = 'Your debt in total is ' + str(total_debts) + '.\n'
    if total_debts != 0:
        message_total += message_details
    return message_total


def get_my_services(message):
    """
    Get all services of a user.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']

    total_services = 0
    message_details = 'Your service for the\n'
    # find user in a list of creditors
    for debt_key_1, debt_value_1 in debts.items():
        for debt_key_2, debt_value_2 in debt_value_1.items():
            if debt_key_2 == uid and debt_value_2 != 0:
                # recalculate value of all services
                total_services += debt_value_2
                message_details += users[debt_key_1].name + ' ' + users[debt_key_1].surname + ' is ' + str(
                    debt_value_2) + '\n'
    message_total = 'Your service in total is ' + str(total_services) + '.\n'
    if total_services != 0:
        message_total += message_details
    return message_total


# TODO: number of verified people
def share(message):
    """
    Share money for all users.

    :param message: user's message.
    :return: reply.
    """

    # get information about the user
    uid = message['from']['id']
    money = int(message['text'].split(' ')[1])

    # number of users
    number_users = len(users)
    # share for each user
    share_money = money / (number_users - 1)

    # update debts dictionary for all users
    for user_uid, user_details in users.items():
        if user_uid != uid:
            alias = user_details.alias
            _change_debts_dictionary(uid=uid, alias=alias, money=share_money)


# TODO: after each method call
def _update_user_dictionary():
    """
    Update users' debts dictionary.
    """
    uids = users.keys()
    for cur_uid_1 in uids:
        # get previous arrears for user
        if cur_uid_1 in debts:
            arrears = debts[cur_uid_1]
        else:
            arrears = {}
        # update arrears for user
        for cur_uid_2 in uids:
            # add zero debt for all users that are currently not in arrears list of a user
            if cur_uid_2 not in arrears and cur_uid_2 != cur_uid_1:
                arrears[cur_uid_2] = 0
        # set new arrears list
        debts[cur_uid_1] = arrears
    # update accordingly to deleted users
    debt_delete_outer = ''
    for debtor, people in debts.items():
        # find deleted debtor
        if debtor not in uids:
            debt_delete_outer = debtor
        debt_delete_inner = ''
        # find deleted person
        for person_uid, value_debt in people.items():
            if person_uid not in uids:
                debt_delete_inner = person_uid
        # remove deleted people
        if debt_delete_inner:
            people.pop(debt_delete_inner)
    # remove deleted debtors
    if debt_delete_outer:
        debts.pop(debt_delete_outer)
