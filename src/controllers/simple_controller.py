import asyncio

from src.database import calender, users
from src.dto.calender_model import (
    Shift,
    ShiftMember, ShiftRequest,
)
from src.dto.users_model import (
    User,
    UserLogin,
    CreateUser,
)
from src.helpers.singleton import (
    SingletonMeta,
)
from datetime import date


class Controller(metaclass=SingletonMeta):
    def __init__(self):
        self.userdb = users
        self.calenderdb = calender

    async def create_user(self, user: CreateUser):
        await self.userdb.create_user(user)

    async def update_user(self, user: User):
        await self.userdb.update_user(user)

    async def login(self, user_login: UserLogin) -> User:
        user = await self.userdb.fetch_user_by_login(user_login)
        return user

    async def check_user_active(self, user: User) -> User:
        user = await self.userdb.fetch_user_by_id(user)
        return user

    async def fetch_all_users(
        self,
    ) -> list[User]:
        return await self.userdb.fetch_all_users()

    async def delete_user(self, user: User):
        await self.userdb.delete_user(user)

    async def create_shift(self, shift: Shift):
        await self.calenderdb.create_shift(shift)

    async def update_shift(self, shift: Shift):
        await self.calenderdb.update_shift(shift)

    async def get_shift(self, shift: Shift):
        shift = await self.calenderdb.fetch_shift(shift)
        return shift

    async def get_shifts_for_month(self, shift_request: ShiftRequest) -> list[Shift]:
        print("hi")
        _calender = await self.calenderdb.fetch_month_shifts(shift_request)
        return _calender

    async def delete_shift(self, shift: Shift):
        await self.calenderdb.delete_shift(shift)

    async def create_shift_member(
        self, shift_member: ShiftMember
    ):
        await self.calenderdb.create_shift_member(
            shift_member
        )

    async def update_shift_member(self, shift_member: ShiftMember):
        await self.calenderdb.update_shift_member(shift_member)

    async def fetch_shift_member(self, shift_member: ShiftMember):
        shift_member = await self.calenderdb.fetch_shift_member(shift_member)
        return shift_member

    async def fetch_all_shift_members(self, shift: Shift) -> list[ShiftMember]:
        shift_members = await self.calenderdb.fetch_all_shift_members(shift)
        return shift_members

    async def delete_shift_member(self, shiftmember: ShiftMember):
        await self.calenderdb.delete_shift_member(shiftmember)


async def main():
    print(":)")


if __name__ == "__main__":
    asyncio.run(main())
