from misc import queries


async def get_users_in_queue_ordered(title):
    """
    Return users joined to queue ordered by surname and name.

    :param title:
    :return:
    """
    users = await queries.get_users_in_queue(title)
    sorted_users = sorted(users, key=lambda x: (x['surname'], x['name']))
    return sorted_users


async def check_presence_queues(titles):
    """
    Check whether all titles specified by user are in queues list.

    :param titles: parsed aliases.
    :return: reply.
    """
    # list of aliases of users that didn't send requests (and string consisting of them)
    fail_validation = []
    fail_validation_str = ''
    # list of aliases of users that sent requests
    queues = await queries.get_queues()
    list_queues_titles = [queue['title'] for queue in queues]
    for title_ in titles:
        if title_ not in list_queues_titles:
            # alias is not present in requests list
            fail_validation.append(title_)
            fail_validation_str += title_ + ' '
    return titles, fail_validation, fail_validation_str


async def check_absence_queues(titles):
    """
    Check whether all titles specified by user are not in queues list.

    :param titles: parsed aliases.
    :return: reply.
    """
    # list of aliases of users that didn't send requests (and string consisting of them)
    fail_validation = []
    fail_validation_str = ''
    # list of aliases of users that sent requests
    queues = await queries.get_queues()
    list_queues_titles = [queue['title'] for queue in queues]
    for title_ in titles:
        if title_ in list_queues_titles:
            # alias is not present in requests list
            fail_validation.append(title_)
            fail_validation_str += title_ + ' '
    return titles, fail_validation, fail_validation_str


async def check_presence_for_user(titles, uid):
    """
    Check whether all titles specified by user are not in list of his/her queues.

    :param titles: parsed aliases.
    :param uid: user id.
    :return: reply.
    """
    # list of aliases of users that didn't send requests (and string consisting of them)
    fail_validation = []
    fail_validation_str = ''
    # get queues of user
    user_queues = await queries.get_my_queues(uid)
    # get titles of user queues
    user_titles = [queue['title'] for queue in user_queues]

    for title_ in user_titles:
        if title_ in user_titles:
            # alias is not present in requests list
            fail_validation.append(title_)
            fail_validation_str += title_ + ' '
    return titles, fail_validation, fail_validation_str
