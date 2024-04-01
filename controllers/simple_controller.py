from database import calender, users
from models.calender_model import Calender, Clearnce_lvl, Shift, ShiftMember
from models.users_model import User, UserLogin
from helpers.singleton import SingletonMeta

class Controller(metaclass=SingletonMeta):
    def __init__(self):
        self.userdb = users.Database()
        self.calenderdb = calender.Database()

    async def create_user(self, user: User):
        await self.userdb.create_user(user)

    async def login(self, user_login: UserLogin) -> User:
        user = await self.userdb.fetch_user(user_login)
        return user

    async def get_shifts(self):
        shifts = await self.calenderdb.fetch_shift()