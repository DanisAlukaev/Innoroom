from misc import queries


async def get_my_debts(message):
    """
    Get all debts of a user.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    name = message['from']['first_name']

    # get debts from the database
    debts = await queries.get_debts(uid)

    # amount of money user owes
    total_debts = 0
    message_details = ''
    for debt in debts:
        value_debt = int(debt['value'])
        if value_debt != 0:
            # increase value of a total debt
            total_debts += value_debt
            # get information about the creditor
            creditor = await queries.get_user_by_id(debt['creditor_id'])
            message_details += '• <b>' + creditor['name'] + ' ' + creditor['surname'] + '</b> is ' + str(value_debt) + '\n'
    if message_details:
        message_details = 'Your debt to the\n' + message_details
    message_total = name + ', your debt in total is ' + str(total_debts) + '.\n\n' + message_details
    return message_total


async def get_my_services(message):
    """
    Get all services of a user.

    :param message: user's message.
    :return: reply.
    """
    # get information about the user
    uid = message['from']['id']
    name = message['from']['first_name']

    # get credits from the database
    credits = await queries.get_credits(uid)

    # amount of money shared with all users
    total_services = 0
    message_details = ''
    for credit in credits:
        value_credit = int(credit['value'])
        if value_credit != 0:
            # increase value of a total debt
            total_services += value_credit
            # get information about the debtor
            debtor = await queries.get_user_by_id(credit['debtor_id'])
            message_details += '• <b>' + debtor['name'] + ' ' + debtor['surname'] + '</b> is ' + str(value_credit) + '\n'
    if message_details:
        message_details = 'Your service for the\n' + message_details
    message_total = name + ', your service in total is ' + str(total_services) + '.\n\n' + message_details
    return message_total
