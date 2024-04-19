import asyncpg
from helpers.singleton import SingletonMeta
from contextlib import asynccontextmanager

# Universal database creator.
# Don't think too much about this class, just be happy it exists.
class BasePool:
    _pools = {}

    def __init__(self, database_name, user, host, password, min_size, max_size):
        self.database_name = database_name
        self.user = user
        self.host = host
        self.password = password
        self.min_size = min_size
        self.max_size = max_size

    async def initialize_pool(self):
        pool_key = f"{self.host}_{self.database_name}"
        if pool_key not in BasePool._pools:
            BasePool._pools[pool_key] = await asyncpg.create_pool(
                database=self.database_name,
                user=self.user,
                host=self.host,
                password=self.password,
                min_size=self.min_size,
                max_size=self.max_size
            )
        return BasePool._pools[pool_key]

    # Contextmanagers is awesome <3
    # Releases the connections by itself
    @asynccontextmanager
    async def acquire(self):
        pool_key = f"{self.host}_{self.database_name}"
        pool = BasePool._pools[pool_key]
        conn = await pool.acquire()
        try:
            yield conn
        finally:
            await pool.release(conn)

    # NEVER use this! It will close a connection, and we will run out fairly quick
    async def close(self):
        pool_key = f"{self.host}_{self.database_name}"
        pool = BasePool._pools[pool_key]
        await pool.close()


# You can freely add more databases by copying PoolUsersData
class PoolUsersData(BasePool, metaclass=SingletonMeta):
    def __init__(self):
        super().__init__(database_name="backend_school",
                         user="firstuser",
                         host="135.181.106.80",
                         password="Studyhard1234.",
                         min_size=1,
                         max_size=20)
