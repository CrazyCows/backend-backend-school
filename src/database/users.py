import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from typing import List, Optional

from src.dto.users_model import User, UserLogin, CreateUser
from src.database.models import User as UserModel
from src.helpers.password_encrypt import Encryption
from src.database.conn_pool import get_async_db_session

Base = declarative_base()


async def create_user(self, user: CreateUser) -> None:
    hashed_password, salt = Encryption().hash_password(user.password)
    async with get_async_db_session() as session:
        new_user = UserModel(
            name=user.name, email=user.email, phone=user.phone,
            role=user.role, username=user.username,
            password=hashed_password, salt=salt)
        session.add(new_user)
        await session.commit()

async def update_user(self, user: User) -> None:
    async with get_async_db_session() as session:
        stmt = select(UserModel).where(UserModel.uid_user == user.uid_user)
        result = await session.execute(stmt)
        db_user = result.scalars().first()
        if db_user:
            db_user.name = user.name
            db_user.email = user.email
            db_user.phone = user.phone
            db_user.role = user.role
            await session.commit()

async def delete_user(self, user: User) -> None:
    async with get_async_db_session() as session:
        stmt = select(UserModel).where(UserModel.uid_user == user.uid_user)
        result = await session.execute(stmt)
        db_user = result.scalars().first()
        if db_user:
            await session.delete(db_user)
            await session.commit()

async def fetch_all_users(self) -> List[User]:
    async with get_async_db_session() as session:
        stmt = select(UserModel)
        result = await session.execute(stmt)
        users = result.scalars().all()
        return [User(uid_user=str(u.uid_user), name=u.name, email=u.email, phone=u.phone, role=u.role) for u in users]

async def fetch_user(self, user: UserLogin, active_user: Optional[User] = None) -> User:
    async with get_async_db_session() as session:
        stmt = select(UserModel).where(UserModel.username == user.username)
        result = await session.execute(stmt)
        db_user = result.scalars().first()
        if db_user and Encryption().verify_password(db_user.password, user.password):
            return User(uid_user=str(db_user.uid_user), name=db_user.name, email=db_user.email,
                        phone=db_user.phone, role=db_user.role)
        else:
            raise Exception("Incorrect username or password")

async def main():

    # Example user data
    create_user = CreateUser(name="test", email="example@mail.com", phone="1234567890", role="admin", username="testuser", password="securepassword")
    user_login = UserLogin(username="testuser", password="securepassword")

    # Example database operations
    await create_user(create_user)
    print(await fetch_user(user_login))

if __name__ == '__main__':
    asyncio.run(main())
