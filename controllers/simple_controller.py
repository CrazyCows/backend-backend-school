from database import calender, users
from models.calender_model import Calender, Clearnce_lvl, Shift, ShiftMember
from models.users_model import User, UserLogin, CreateUser
from helpers.singleton import SingletonMeta
from datetime import date

class Controller(metaclass=SingletonMeta):
    def __init__(self):
        self.userdb = users.Database()
        self.calenderdb = calender.Database()

    async def create_user(self, user: CreateUser):
        await self.userdb.create_user(user)

    async def login(self, user_login: UserLogin) -> User:
        user = await self.userdb.fetch_user(user_login)
        return user

    async def fetch_all_users(self) -> list[User]:
        return await self.userdb.fetch_all_users()

    async def delete_user(self, user: User):
        await self.userdb.delete_user(user)

    async def create_shift(self, shift: Shift):
        await self.calenderdb.create_shift(shift)
    async def get_shift(self, shift: Shift):
        shift = await self.calenderdb.fetch_shift(shift)
        return shift

    async def get_shifts_for_month(self, date: date, user: User):
        calender = await self.calenderdb.fetch_month_shifts(date, user)
        return calender

    async def delete_shift(self, shift: Shift):
        await self.calenderdb.delete_shift(shift)