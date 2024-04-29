import asyncio

from src.database.conn_pool import (
    PoolUsersData,
)
from src.models.users_model import (
    User,
    UserLogin,
    CreateUser,
)
from src.helpers.password_encrypt import (
    Encryption,
)
from typing import List
from src.database.models import (
    users,
    db,
)
from datetime import datetime


# This is just an example to show how to use the pool and the database connection - database does not exist yet
# Transactions is used for deletes and inserts to prevent the data from being read when modified.
class Database:
    def __init__(self):
        self.pool = PoolUsersData()

    async def create_user(self, user: CreateUser) -> None:
        async with db.atomic_async():
            hashed_password, salt = Encryption().hash_password(user.password)
            await users.get_or_create(
                uid_user=user.uid_user,
                name=user.name,
                email=user.email,
                phone=user.phone,
                role=user.role,
                username=user.username,
                last_login=datetime.now(),
                registration=datetime.now(),
                last_modified=datetime.now(),
                salt=salt,
                password=hashed_password,
            )

    async def update_user(self, user: User) -> None:
        async with db.atomic_async():
            await (
                users.update(
                    name=user.name,
                    email=user.email,
                    phone=user.phone,
                    role=user.role,
                )
                .where(users.uid_user == user.uid_user)
                .execute()
            )

    async def delete_user(self, user: User) -> None:
        async with db.atomic_async():
            await users.delete().where(users.uid_user == user.uid_user).execute()

    async def fetch_all_users(
        self,
    ) -> List[User]:
        async with db.atomic_async():
            all_users = await users.select()
            return [user for user in all_users]

    async def fetch_user(
        self,
        user: UserLogin,
        active_user: User = None,
    ) -> User:
        async with db.atomic_async():
            user_query = users.select().where((users.username == user.username) | (users.uid_user == user.uid_user))

            if active_user is None:
                user = await user_query.get()
                correct_password = Encryption().verify_password(
                    user.password,
                    user.password,
                )
                if not correct_password:
                    raise Exception("Incorrect password")
                return user
            else:
                user_query = user_query.where(users.uid_user == active_user.uid_user)
                return await user_query.get()

    async def fetch_user_by_id(self, user: User) -> User:
        async with db.atomic_async():
            user = await users.get_or_none(users.uid_user == user.uid_user)
            if not user:
                raise Exception("User not found")
            return user


async def main():
    base_pool = await PoolUsersData().initialize_pool()
    database = Database()

    """
    name: str
    email: str
    phone: Optional[str] = None
    role: str
    username: str
    password: str"""
    create_user = CreateUser(
        name="test",
        email="<MAIL>",
        phone="<PHONE>",
        role="admin",
        username="test",
        password="<PASSWORD>",
    )

    user_login = UserLogin(
        username="test",
        password="<PASSWORD>",
    )

    print(await database.fetch_user(user_login))


if __name__ == "__main__":
    asyncio.run(main())
