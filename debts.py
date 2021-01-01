from users import users, alias_dict, uid_dict, get_list_user_aliases
import re

# users' debts
debts = {}


def me(message):
    """
    Display information about the user.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    message_me = users[uid].__str__()

    # amount of money user owes
    total_debts = 0
    for creditor, value in debts[uid].items():
        if value != 0:
            # increase value of a total debt
            total_debts += value
    message_me += '\n\n<b>Finances</b>\nTotal debt: ' + str(total_debts) + '.\n'

    # amount of money shared with all users
    total_services = 0
    # find user in a list of creditors
    for debtor, people in debts.items():
        for creditor, value_debt in people.items():
            if creditor == uid and value_debt != 0:
                total_services += value_debt
    message_me += 'Total service: ' + str(total_services) + '.'
    return message_me


def give(message):
    """
    Give debt for specified users.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    alias = message['from']['username']

    if re.fullmatch(r'/give [1-9]+[0-9]*( @\w+)+', message['text']):
        # message is properly formatted

        # get amount of give money
        money = int(message['text'].split(' ')[1])
        # get list of aliases from message
        aliases = message['text'].replace('@', '').split(' ')[2:]

        # list and string of aliases that didn't pass verification
        fail_verification = []
        fail_verification_str = ''
        # get list of user aliases
        list_user_aliases = get_list_user_aliases()
        for alias_ in aliases:
            # check whether alias belongs to the user of bot
            if alias_ not in list_user_aliases:
                fail_verification.append(alias_)
                fail_verification_str += '@' + alias_ + ' '

        if len(fail_verification) == 0:
            # all aliases are in users list

            # amount on money per each user
            share_give = money / len(aliases)
            # string with aliases of debtors
            aliases_str = ''
            for alias_ in aliases:
                aliases_str += '@' + alias_ + ' '
                # update debts dictionary
                _change_debts_dictionary(uid=uid, alias=alias_, money=share_give)
            message_give = '@' + alias + ', you have given ' + str(share_give) + ' to ' + aliases_str
        else:
            # some aliases fail validation
            message_give = 'User with alias(es) ' + fail_verification_str + 'do(es) not registered in bot.'
    else:
        # message fails to parse
        message_give = 'Message does not match the required format. Check rules in /help.'
    return message_give


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


def get_my_debts(message):
    """
    Get all debts of a user.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    alias = alias_dict[uid]

    # amount of money user owes
    total_debts = 0
    message_details = 'Your debt to the\n'
    for creditor, value in debts[uid].items():
        if value != 0:
            # increase value of a total debt
            total_debts += value
            message_details += users[creditor].name + ' ' + users[creditor].surname + ' is ' + str(value) + '\n'
    message_total = '@' + alias + ', your debt in total is ' + str(total_debts) + '.\n'
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
    alias = alias_dict[uid]

    # amount of money shared with all users
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
    message_total = '@' + alias + ', your service in total is ' + str(total_services) + '.\n'
    if total_services != 0:
        message_total += message_details
    return message_total


def share(message):
    """
    Share money for all users.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']

    if re.fullmatch(r'/share [1-9]+[0-9]*', message['text']):
        # message is properly formatted

        # get amount of money from user
        money = int(message['text'].split(' ')[1])
        # number of bot's users
        number_users = len(users)
        # amount on money per each user
        share_money = money / (number_users - 1)

        # update debts dictionary for all users
        for user_uid, user_details in users.items():
            if user_uid != uid:
                # all users except creditor
                alias = user_details.alias
                _change_debts_dictionary(uid=uid, alias=alias, money=share_money)
        message_share = '@' + alias_dict[uid] + ' ' + str(money) + ' was shared among all users of the bot.'
    else:
        # message fails to parse
        message_share = 'Message does not match the required format. Check rules in /help.'
    return message_share


def update_user_dictionary():
    """
    Update users' debts dictionary.
    """
    uids = users.keys()
    for user1 in uids:
        # get previous arrears for user
        if user1 in debts:
            arrears = debts[user1]
        else:
            arrears = {}
        # update arrears for user
        for user2 in uids:
            # add zero debt for all users that are currently not in arrears list of a user
            if user2 not in arrears and user2 != user1:
                arrears[user2] = 0
        # set new arrears list
        debts[user1] = arrears

    # update accordingly to deleted users
    debt_delete_outer = ''
    for debtor, people in debts.items():
        # find deleted debtor
        if debtor not in uids:
            debt_delete_outer = debtor
        debt_delete_inner = ''
        # find deleted person
        for creditor, value_debt in people.items():
            if creditor not in uids:
                debt_delete_inner = creditor
        # remove deleted people
        if debt_delete_inner:
            people.pop(debt_delete_inner)

    # remove deleted debtors
    if debt_delete_outer:
        debts.pop(debt_delete_outer)
