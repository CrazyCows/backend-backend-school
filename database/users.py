from database.conn_pool import PoolUsersData
from models.users_model import User, UserLogin, CreateUser
from typing import List

# This is just an example to show how to use the pool and the database connection - database does not exist yet
# Transactions is used for deletes and inserts to prevent the data from being read when modified.
class Database:
    def __init__(self):
        self.pool = PoolUsersData()


    async def create_user(self, user: CreateUser) -> User:
        async with self.pool.acquire() as conn:
            try:
                with conn.cursor() as cur:
                    create_statement = ("INSERT INTO users(name, email, phone, role, username, password) "
                                        "VALUES ($1, $2, $3, $4, $5, $6) ON CONFLICT DO NOTHING")
                    params = [user.user_name, user.email, user.phone, user.role, user.username, user.password]
                    await conn.execute(create_statement, params)
            except Exception as e:
                print("define a propper exception")
                print(e)


    async def update_user(self, user: User):
        async with self.pool.acquire() as conn:
            try:
                update_statement = "UPDATE users SET name = $2, email = $3, phone = $4, role = $5 WHERE uid_user=$1"
                params = [user.user_uid, user.user_name, user.email, user.phone, user.role]
                await conn.execute(update_statement, params)
            except Exception as e:
                print("define proper exception: \n", e)
        raise NotImplementedError("Mangler implementation")


    async def delete_user(self, user: User):
        async with self.pool.acquire() as conn:
            try:
                delete_statement = "DELETE FROM users WHERE users.uid_user = $1"
                params = user.user_uid
                await conn.execute(delete_statement, params)
            except Exception as e:
                print("define proper exception: \n", e)
        raise NotImplementedError("Mangler implementation")

    async def fetch_all_users(self) -> List[User]:
        async with self.pool.acquire() as conn:
            try:
                query = "SELECT users.uid_user, users.name, users.email, users.phone, users.role FROM users"
                result = await conn.execute(query)
                users = [User(user_uid=user.get('uid_user'),
                              user_name=user.get('name'),
                              email=user.get('email'),
                              phone=result.get('phone'),
                              role=user.get('role')) for user in result]
                return users
            except Exception as e:
                print("Make proper exception:", e)

    async def fetch_user(self, user: UserLogin) -> User:
        async with self.pool.acquire() as conn:
            try:
                query = "SELECT users.uid_user, users.name, users.email, users.phone, users.role FROM users WHERE users.password=$1 and users.username=$2"
                params = [user.password, user.username]
                result = await conn.fetchrow(query, params)
                user = User(user_uid=result.get('uid_user'),
                            user_name=result.get('name'),
                            email=result.get('email'),
                            phone=result.get('phone'),
                            role=result.get('role'))
                return user
            except Exception as e:
                print("Make proper exception")