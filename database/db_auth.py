import asyncio
from database.conn_pool import PoolUsersData


# This is just an example to show how to use the pool and the database connection - database does not exist yet
# Transactions is used for deletes and inserts to prevent the data from being read when modified.
class Database:
    def __init__(self):
        self.pool = PoolUsersData()

    async def create_user(self, user_id: str, email: str) -> bool:
        try:
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    query = """INSERT INTO users (user_id, email) VALUES ($1, $2)"""
                    params = [user_id, email]
                    await conn.execute(query, params)

                    query = """INSERT INTO users_folders(user_id, folder_name) VALUES ($1, $2)"""
                    params = [user_id, 'static']
                    await conn.execute(query, params)

            return True
        except:
            return False

    # Deleted a user - x
    async def delete_user(self, user_id: str) -> bool:
        try:
            async with self.pool.acquire as conn:
                async with conn.transaction():
                    query3 = """DELETE FROM users CASCADE WHERE username = $1"""
                    params = [user_id]
                    await conn.execute(query3, params)

            return True
        except:
            return False



