from asyncpg import Connection
from asyncpg.exceptions import UniqueViolationError


class Queries:
    # table users

    ADD_REQUEST = "INSERT INTO users(uid, alias, name, surname, request) VALUES ($1, $2, $3, $4, 'pending')"
    GET_REQUESTS = "SELECT * FROM users WHERE request = 'pending'"
    ACCEPT_REQUEST = "UPDATE users SET request = 'accepted' WHERE alias = $1"
    UPDATE_ALIAS = "UPDATE users SET alias = $1 WHERE uid = $2"
    UPDATE_NAME = "UPDATE users SET name = $1 WHERE uid = $2"
    UPDATE_SURNAME = "UPDATE users SET surname = $1 WHERE uid = $2"
    GET_USERS = "SELECT * FROM users WHERE request = 'accepted'"
    GET_USER_BY_UID = "SELECT * FROM users WHERE uid = $1"
    GET_USER_BY_ID = "SELECT * FROM users WHERE id = $1"
    GET_USER_BY_ALIAS = "SELECT * FROM users WHERE alias = $1"
    REMOVE_USER_BY_ALIAS = "DELETE FROM users WHERE alias = $1"
    REMOVE_USER_BY_UID = "DELETE FROM users WHERE uid = $1"

    # table queues

    CREATE_QUEUE = "INSERT INTO queues(title) VALUES ($1)"
    GET_QUEUES = "SELECT * FROM queues ORDER BY title"
    GET_QUEUE_ID_BY_TITLE = "SELECT id FROM queues WHERE title = $1"
    GET_MY_QUEUES = "SELECT title FROM (queues LEFT JOIN members ON queues.id = members.queue_id) WHERE user_id = " \
                    "(SELECT id FROM users WHERE uid = $1) ORDER BY title"
    REMOVE_QUEUE_BY_TITLE = "DELETE FROM queues WHERE id = (SELECT id FROM queues WHERE title = $1)"

    # table members

    JOIN_QUEUE = "INSERT INTO members(user_id, queue_id) VALUES ($1, $2)"
    REMOVE_MEMBER = "DELETE FROM members WHERE user_id = (SELECT id FROM users WHERE uid = $1)"
    GET_USERS_IN_QUEUE = "SELECT * FROM users WHERE id = (SELECT user_id FROM members WHERE queue_id = " \
                         "(SELECT id FROM queues WHERE title = $1))"
    GET_CURRENT_USER_INDEX = "SELECT curr_user FROM queues WHERE title = $1"
    CHANGE_SKIPS_FOR_USER = "UPDATE members SET skips = $1 WHERE user_id = (SELECT id FROM users WHERE uid = $2)"
    CHANGE_NEXT_USER = "UPDATE queues SET curr_user = $1 WHERE title = $2"
    GET_SKIPS_FOR_USER = "SELECT skips FROM members WHERE user_id = (SELECT id FROM users WHERE uid = $1)"

    # table debts

    CREATE_ZERO_DEBT = "INSERT INTO debts(debtor_id, creditor_id, value) " \
                       "VALUES ((SELECT id FROM users WHERE uid = $1), (SELECT id FROM users WHERE uid = $2), 0)"
    GET_DEBTS = "SELECT * FROM debts WHERE debtor_id = (SELECT id FROM users WHERE uid = $1)"
    GET_DEBT = "SELECT value FROM debts WHERE debtor_id = (SELECT id FROM users WHERE uid = $1) and " \
               "creditor_id = (SELECT id FROM users WHERE uid = $2)"
    GET_CREDITS = "SELECT * FROM debts WHERE creditor_id = (SELECT id FROM users WHERE uid = $1)"
    UPDATE_DEBT = "UPDATE debts SET value = $1 WHERE debtor_id = (SELECT id FROM users WHERE uid = $2)" \
                  " and creditor_id = (SELECT id FROM users WHERE uid = $3)"

    def __init__(self, db):
        self.pool: Connection = db

    # table users

    async def add_request(self, uid, alias, name, surname):
        args = uid, alias, name, surname
        command = self.ADD_REQUEST
        try:
            await self.pool.fetchval(command, *args)
        except UniqueViolationError:
            pass

    async def get_requests(self):
        requests = await self.pool.fetch(self.GET_REQUESTS)
        return requests

    async def accept_request(self, alias):
        await self.pool.fetchval(self.ACCEPT_REQUEST, alias)

    async def update_alias(self, alias, uid):
        args = alias, uid
        command = self.UPDATE_ALIAS
        await self.pool.fetch(command, *args)

    async def update_name(self, name, uid):
        args = name, uid
        command = self.UPDATE_NAME
        await self.pool.fetch(command, *args)

    async def update_surname(self, surname, uid):
        args = surname, uid
        command = self.UPDATE_SURNAME
        await self.pool.fetch(command, *args)

    async def get_users(self):
        users = await self.pool.fetch(self.GET_USERS)
        return users

    async def get_user_by_uid(self, uid):
        user = (await self.pool.fetch(self.GET_USER_BY_UID, uid))[0]
        return user

    async def get_user_by_id(self, id):
        user = (await self.pool.fetch(self.GET_USER_BY_ID, id))[0]
        return user

    async def get_user_by_alias(self, alias):
        user = (await self.pool.fetch(self.GET_USER_BY_ALIAS, alias))[0]
        return user

    async def remove_user_by_alias(self, alias):
        await self.pool.fetchval(self.REMOVE_USER_BY_ALIAS, alias)

    async def remove_user_by_uid(self, uid):
        await self.pool.fetchval(self.REMOVE_USER_BY_UID, uid)

    # table queues

    async def create_queue(self, title):
        queues = await self.pool.fetch(self.CREATE_QUEUE, title)
        return queues

    async def get_queues(self):
        queues = await self.pool.fetch(self.GET_QUEUES)
        return queues

    async def get_queue_id_by_title(self, title):
        queue = (await self.pool.fetch(self.GET_QUEUE_ID_BY_TITLE, title))[0]
        return queue

    async def get_my_queues(self, uid):
        queues = await self.pool.fetch(self.GET_MY_QUEUES, uid)
        return queues

    async def remove_queue_by_title(self, title):
        await self.pool.fetchval(self.REMOVE_QUEUE_BY_TITLE, title)

    # table members

    async def join_queue(self, user_id, queue_id):
        args = user_id, queue_id
        await self.pool.fetch(self.JOIN_QUEUE, *args)

    async def quit_queue(self, uid):
        await self.pool.fetch(self.REMOVE_MEMBER, uid)

    async def get_users_in_queue(self, title):
        users = await self.pool.fetch(self.GET_USERS_IN_QUEUE, title)
        return users

    async def get_current_user_index(self, title):
        index = (await self.pool.fetch(self.GET_CURRENT_USER_INDEX, title))[0]['curr_user']
        return index

    async def change_skips_for_user(self, skips, uid):
        args = skips, uid
        await self.pool.fetch(self.CHANGE_SKIPS_FOR_USER, *args)

    async def change_next_user(self, index, title):
        args = index, title
        await self.pool.fetch(self.CHANGE_NEXT_USER, *args)

    async def get_skips_for_user(self, uid):
        skips = await self.pool.fetch(self.GET_SKIPS_FOR_USER, uid)
        return skips

    # table debts

    async def create_zero_debt(self, debtor_id, creditor_id):
        args = debtor_id, creditor_id
        await self.pool.fetch(self.CREATE_ZERO_DEBT, *args)

    async def get_debts(self, uid):
        debts = await self.pool.fetch(self.GET_DEBTS, uid)
        return debts

    async def get_debt(self, debtor_uid, creditor_uid):
        args = debtor_uid, creditor_uid
        debt = (await self.pool.fetch(self.GET_DEBT, *args))[0]
        return debt

    async def update_debt(self, value, debtor_uid, creditor_uid):
        args = value, debtor_uid, creditor_uid
        await self.pool.fetch(self.UPDATE_DEBT, *args)

    async def get_credits(self, uid):
        debts = await self.pool.fetch(self.GET_CREDITS, uid)
        return debts
