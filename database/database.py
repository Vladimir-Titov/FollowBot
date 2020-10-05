import os

import asyncpg


class Database:
    pool = None

    @classmethod
    async def create_pool(cls):
        cls.pool = await asyncpg.create_pool(dsn=os.environ['DATABASE_URL'])
        return cls.pool


class Query(Database):

    @staticmethod
    async def execute(sql: str, *args, **kwargs):
        async with Query().pool.acquire() as connection:
            return await connection.fetch(sql, *args, **kwargs)

