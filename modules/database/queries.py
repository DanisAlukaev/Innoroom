from asyncpg import Connection
from asyncpg.exceptions import UniqueViolationError
from aiogram import types
import logging


class Queries:
    # Users queries
    ADD_REQUEST = "INSERT INTO users(uid, alias, name, surname, request) VALUES ($1, $2, $3, $4, 'pending')"
    ACCEPT_USER = "UPDATE users SET request = 'accepted' WHERE alias = $1"
    REMOVE_USER = "DELETE FROM users WHERE alias = $1"
    UPDATE_ALIAS = "UPDATE users SET alias = $1 WHERE uid = $2"
    UPDATE_NAME = "UPDATE users SET name = $1 WHERE uid = $2"
    UPDATE_SURNAME = "UPDATE users SET surname = $1 WHERE uid = $2"
    GET_USERS = "SELECT * FROM users WHERE request = 'accepted'"
    GET_REQUESTS = "SELECT * FROM users WHERE request = 'pending'"
    GET_UID_BY_ALIAS = "SELECT uid FROM users WHERE alias = $1 and request = 'accepted'"
    GET_BY_UID = "SELECT * FROM users WHERE uid = $1"
    # Queues queries
    CREATE_QUEUE = "INSERT INTO queues(title) VALUES ($1)"
    GET_QUEUE_ID_BY_TITLE = "SELECT id FROM queues WHERE title = $1"
    JOIN_QUEUE = "INSERT INTO members(user_id, queue_id) VALUES ($1, $2)"
    QUIT_QUEUE = "DELETE FROM members WHERE user_id = $1"
    REMOVE_QUEUE = "DELETE FROM queues WHERE id = $1"
    GET_QUEUES = "SELECT * FROM queues"
    USER_QUEUES = "SELECT title FROM queues WHERE id = (SELECT queue_id FROM members WHERE user_id = $1)"
    GET_USERS_IN_QUEUE_ORDERED = "SELECT user_id FROM members WHERE queue_id = $1"
    GET_CURRENT_USER_INDEX = "SELECT curr_user FROM queues WHERE title = $1"
    NEXT_USER = "UPDATE queues SET curr_user = $1 WHERE title = $2"
    GET_SKIPS_FOR_USER = "SELECT skips FROM members WHERE user_id = $1"
    CHANGE_SKIPS_FOR_USER = "UPDATE members SET skips = $1 WHERE user_id = $2"
    # Debts queries
    GIVE = "INSERT INTO debts(debtor_id, creditor_id, value) VALUES ($1, $2)"
    GET_DEBTS = "SELECT * FROM debts WHERE debtor_id = $1"
    GET_DEBT = "SELECT value FROM debts WHERE debtor_id = $1 and creditor_id = $2"
    GET_CREDITS = "SELECT debtor_id, value FROM debts WHERE creditor_id = $1"
    UPDATE_DEBT = "UPDATE debts SET value = $1 WHERE debtor_id = $2 and creditor_id = $3"

    def __init__(self, db):
        self.pool: Connection = db

    async def add_request(self, uid, alias, name, surname):
        args = uid, alias, name, surname
        command = self.ADD_REQUEST
        try:
            await self.pool.fetchval(command, *args)
            return True
        except UniqueViolationError:
            return False

    async def accept_request(self, alias):
        await self.pool.fetchval(self.ACCEPT_USER, alias)

    async def decline_request(self, alias):
        await self.pool.fetchval(self.REMOVE_USER, alias)

    async def get_by_uid(self, uid):
        user = await self.pool.fetch(self.GET_BY_UID, uid)
        return user

    async def get_users(self):
        users = await self.pool.fetch(self.GET_USERS)
        return users

    async def get_requests(self):
        requests = await self.pool.fetch(self.GET_REQUESTS)
        return requests

    async def update_alias(self, alias, uid):
        args = alias, uid
        command = self.UPDATE_ALIAS
        requests = await self.pool.fetch(command, *args)
        return requests

    async def update_name(self, name, uid):
        args = name, uid
        command = self.UPDATE_NAME
        requests = await self.pool.fetch(command, *args)
        return requests

    async def update_surname(self, surname, uid):
        args = surname, uid
        command = self.UPDATE_SURNAME
        requests = await self.pool.fetch(command, *args)
        return requests
