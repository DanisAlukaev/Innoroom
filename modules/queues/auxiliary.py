from misc import queries
import logging


async def get_users_in_queue_ordered(title):
    """
    Return users joined to queue ordered by surname and name.

    :param title:
    :return:
    """
    users = await queries.get_users_in_queue(title)
    sorted_users = sorted(users, key=lambda x: (x['surname'], x['name']))
    return sorted_users
