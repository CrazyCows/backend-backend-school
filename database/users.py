import asyncio

from database.conn_pool import PoolUsersData
from models.users_model import User, UserLogin, CreateUser
from helpers.password_encrypt import Encryption
from typing import List

# This is just an example to show how to use the pool and the database connection - database does not exist yet
# Transactions is used for deletes and inserts to prevent the data from being read when modified.
class Database:
    def __init__(self):
        self.pool = PoolUsersData()

    async def create_user(self, user: CreateUser) -> None:
        hashed_password, salt = Encryption().hash_password(user.password)
        async with self.pool.acquire() as conn:
            create_statement = ("INSERT INTO users(name, email, phone, role, username, password, salt) "
                                "VALUES ($1, $2, $3, $4, $5, $6, $7) ON CONFLICT DO NOTHING")
            params = [user.name, user.email, user.phone, user.role, user.username, hashed_password, salt]
            await conn.execute(create_statement, *params)

    async def update_user(self, user: User) -> None:
        async with self.pool.acquire() as conn:
            update_statement = "UPDATE users SET name = $2, email = $3, phone = $4, role = $5 WHERE uid_user=$1"
            params = [user.uid_user, user.name, user.email, user.phone, user.role]
            await conn.execute(update_statement, *params)

    async def delete_user(self, user: User) -> None:
        async with self.pool.acquire() as conn:
            delete_statement = "DELETE FROM users WHERE users.uid_user = $1"
            params = user.uid_user
            await conn.execute(delete_statement, params)

    async def fetch_all_users(self) -> List[User]:
        async with self.pool.acquire() as conn:
            query = "SELECT users.uid_user, users.name, users.email, users.phone, users.role FROM users"
            result = await conn.execute(query)
            users = [User(uid_user=user.get('uid_user'),
                          user_name=user.get('name'),
                          email=user.get('email'),
                          phone=result.get('phone'),
                          role=user.get('role')) for user in result]
            return users

    async def fetch_user(self, user: UserLogin, active_user: User = None) -> User:
        async with self.pool.acquire() as conn:

            query = "SELECT users.password, users.uid_user, users.name, users.email, users.phone, users.role FROM users WHERE users.username=$1 or users.uid_user=$2"
            params = [user.username, active_user.uid_user if active_user else None]
            result = await conn.fetchrow(query, *params)

            if active_user is None:
                correct_password = Encryption().verify_password(result.get('password'), user.password)
                if correct_password is False:
                    raise Exception("false password")
            print(result)
            print(result.get('uid_user'))

            user = User(uid_user=str(result.get('uid_user')),
                        name=result.get('name'),
                        email=result.get('email'),
                        phone=result.get('phone'),
                        role=result.get('role'))
            return user

async def main():
    base_pool = await PoolUsersData().initialize_pool()
    database = Database()

    '''
    name: str
    email: str
    phone: Optional[str] = None
    role: str
    username: str
    password: str'''
    create_user = CreateUser(name="test", email="<MAIL>", phone="<PHONE>", role="admin", username="test",
                             password="<PASSWORD>")

    user_login = UserLogin(username="test", password="<PASSWORD>")

    print(await database.fetch_user(user_login))



if __name__ == '__main__':
    asyncio.run(main())
