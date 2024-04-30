import asyncio

import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from typing import List, Optional

from src.dto.users_model import User, UserLogin, CreateUser
from src.database.models import UserORM as UserModel, ClearanceLevelORM
from src.helpers.password_encrypt import Encryption
from src.database.conn_pool import get_async_db_session, get_db_session

Base = sqlalchemy.orm.declarative_base()


async def create_user(user: CreateUser) -> None:
    hashed_password = Encryption().hash_password(user.password)
    print(hashed_password)
    async with get_async_db_session() as session:
        new_user = UserModel(
            name=user.name, email=user.email, phone=user.phone,
            role=user.role, username=user.username,
            password=hashed_password)
        session.add(new_user)
        await session.commit()

def create_user_sync(user: CreateUser) -> None:
    hashed_password = Encryption().hash_password(user.password)
    print(hashed_password)
    with get_db_session() as session:
        new_user = UserModel(
            name=user.name, email=user.email, phone=user.phone,
            role=user.role, username=user.username,
            password=hashed_password)
        session.add(new_user)
        session.commit()

"""
    id SERIAL PRIMARY KEY NOT NULL,
    uid_clearance UUID UNIQUE DEFAULT uuid_generate_v4(),
    role VARCHAR(100) UNIQUE NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
"""

async def create_clearence_level(clearence_role: str) -> None:
    clearence_level = ClearanceLevelORM(role=clearence_role)
    async with get_async_db_session() as session:
        session.add(clearence_level)
        await session.commit()

def create_clearence_level_sync(clearence_role: str) -> None:
    clearence_level = ClearanceLevelORM(role=clearence_role)
    with get_db_session() as session:
        session.add(clearence_level)
        session.commit()

async def update_user(user: User) -> None:
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

async def delete_user(user: User) -> None:
    async with get_async_db_session() as session:
        stmt = select(UserModel).where(UserModel.uid_user == user.uid_user)
        result = await session.execute(stmt)
        db_user = result.scalars().first()
        if db_user:
            await session.delete(db_user)
            await session.commit()

async def fetch_all_users() -> List[User]:
    async with get_async_db_session() as session:
        stmt = select(UserModel)
        result = await session.execute(stmt)
        users = result.scalars().all()
        return [User(uid_user=str(u.uid_user), name=u.name, email=u.email, phone=u.phone, role=u.role) for u in users]

async def fetch_user(user: UserLogin) -> User:
    async with get_async_db_session() as session:
        print("--------------- DATABASE ---------------")
        stmt = select(UserModel).where(UserModel.username == user.username)
        result = await session.execute(stmt)
        db_user = result.scalars().first()
        print(db_user)
        print()
        if db_user and Encryption().verify_password(db_user.password, user.password):
            return User(uid_user=str(db_user.uid_user), name=db_user.name, email=db_user.email,
                        phone=db_user.phone, role=db_user.role)
        else:
            raise Exception("Incorrect username or password")

async def main():
    await create_clearence_level("admin")
    # Example user data
    createuser = CreateUser(name="test2", email="example@gmail.com", phone="12345679", role="admin", username="testuser2", password="securepassword2")
    #user_login = UserLogin(username="testuser", password="securepassword")

    # Example database operations

    #await create_user(createuser)
    user_login = UserLogin(username="testuser2", password="securepassword2")
    print(await fetch_user(user_login))

if __name__ == '__main__':
    asyncio.run(main())
