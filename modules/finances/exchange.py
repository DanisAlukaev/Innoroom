from misc import queries
import re
from modules.users import auxiliary


async def _change_debts_dictionary(debtor_uid, creditor_uid, money):
    """
    Update table debts.

    :param debtor_uid: user id of a creditor.
    :param creditor_uid: user id of a debtor.
    :param money: credit.
    """
    debt_of_creditor = int((await queries.get_debt(creditor_uid, debtor_uid))['value'])
    # check whether debt of a creditor is 0
    if debt_of_creditor == 0:
        await queries.update_debt(money, debtor_uid, creditor_uid)
    # debt of a creditor is less than a given credit
    elif debt_of_creditor <= money:
        await queries.update_debt(money - debt_of_creditor, debtor_uid, creditor_uid)
        await queries.update_debt(0, creditor_uid, debtor_uid)
    # debt of a creditor is greater than a given credit
    elif debt_of_creditor > money:
        current_debt_of_creditor = int((await queries.get_debt(creditor_uid, debtor_uid))['value'])
        await queries.update_debt(current_debt_of_creditor - money, creditor_uid, debtor_uid)
        await queries.update_debt(0, debtor_uid, creditor_uid)


async def give(message):
    """
    Give debt for specified users.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    name = message['from']['first_name']

    if not re.fullmatch(r'/give [1-9]+[0-9]*( @\w+)+', message['text']):
        # message fails to parse
        return 'Message does not match the required format. Check rules in /help.'

    # get amount of give money
    money = int(message['text'].split(' ')[1])
    # get list of aliases from message
    aliases_raw = message['text'].replace('@', '').split(' ')[2:]

    # get parsed aliases and aliases that were failed to validate
    aliases, fail_verification, fail_verification_str = await auxiliary.check_presence_users(aliases_raw)

    if message['from']['username'] in aliases:
        return 'You cannot lend money to yourself twice!'

    if len(fail_verification) != 0:
        # some aliases fail validation
        return 'User with alias(es) ' + fail_verification_str + 'do(es) not registered in bot.'

    # amount on money per each user
    share_give = money / (len(aliases) + 1)
    # string with aliases of debtors
    aliases_str = ''
    for alias_ in aliases:
        aliases_str += '@' + alias_ + ' '
        # get user id of debtor
        debtor_uid = (await queries.get_user_by_alias(alias_))['uid']
        # update table debts
        await _change_debts_dictionary(debtor_uid, uid, share_give)
    message_give = name + ', you have given ' + str(share_give) + ' to ' + aliases_str
    return message_give


async def share(message):
    """
    Share money for all users.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    name = message['from']['first_name']

    if not re.fullmatch(r'/share [1-9]+[0-9]*', message['text']):
        # message fails to parse
        return 'Message does not match the required format. Check rules in /help.'

    # get amount of money from message
    money = int(message['text'].split(' ')[1])
    # number of users
    users = await queries.get_users()
    number_users = len(users)
    # amount on money per each user
    share_money = money / number_users

    # update table debts for all users except creditor
    for user in users:
        if user['uid'] != uid:
            # all users except creditor
            debtor_uid = user['uid']
            # update table debts
            await _change_debts_dictionary(debtor_uid, uid, share_money)
    message_share = name + ', ' + str(money) + ' was shared among all users of the bot.'
    return message_share
