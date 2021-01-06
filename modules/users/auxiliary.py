from misc import queries
import logging


async def get_user_ids():
    users = await queries.get_users()
    ids = [user['uid'] for user in users]
    return ids


async def get_request_ids():
    requests = await queries.get_requests()
    ids = [request['uid'] for request in requests]
    return ids


async def user_data_to_string(uid):
    users_data = await queries.get_by_uid(uid)
    if users_data[0]['request'] == 'pending':
        profile = '<b>Request profile:</b>\n'
    else:
        profile = '<b>Profile account:</b>\n'
    profile += 'Alias: @' + users_data[0]['alias'] + '\n' + 'Name: ' + users_data[0][
        'name'] + '\n' + 'Surname: ' + users_data[0]['surname']
    return profile


async def check_presence_requests(message):
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
    requests = await queries.get_requests()
    list_request_aliases = [request['alias'] for request in requests]
    for alias_ in aliases:
        if alias_ not in list_request_aliases:
            # alias is not present in requests list
            fail_validation.append(alias_)
            fail_validation_str += '@' + alias_ + ' '
    return aliases, fail_validation, fail_validation_str
