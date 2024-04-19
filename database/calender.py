import asyncio

from database.conn_pool import PoolUsersData
from models.calender_model import Shift, Calender, ShiftMember
from datetime import date, datetime

from models.users_model import User, CreateUser, UserLogin

from database.users import Database as users_database


# This is just an example to show how to use the pool and the database connection - database does not exist yet
# Transactions is used for deletes and inserts to prevent the data from being read when modified.
class Database:
    def __init__(self):
        self.pool = PoolUsersData()

    async def create_shift(self, shift: Shift) -> Shift:
        async with self.pool.acquire() as conn:
            create_statement = "INSERT INTO shifts(start_time, end_time, active) VALUES ($1, $2, $3)"
            params = [shift.start_time, shift.end_time, shift.active]
            await conn.execute(create_statement, *params)

    async def update_shift(self, shift: Shift):
        async with self.pool.acquire() as conn:
            update_statement = ("UPDATE shifts SET start_time = $2, end_time = $3, "
                                "active = $4 WHERE uid_shift = $1")
            params = [shift.uid_shift, shift.start_time, shift.end_time, shift.active]
            await conn.execute(update_statement, *params)

    async def delete_shift(self, shift: Shift):
        async with self.pool.acquire() as conn:
            query = "DELETE FROM shifts WHERE shifts.uid_shift=$1"
            params = shift.uid_shift
            await conn.execute(query, *params)

    async def fetch_shift(self, shift: Shift) -> Shift:
        async with self.pool.acquire() as conn:
            query = "SELECT * FROM shifts WHERE uid_shift = $1"
            params = shift.uid_shift
            results = await conn.fetch(query, *params)
            return results

    # TODO: This can't be right(?)
    async def fetch_month_shifts(self, date: date, user: User) -> Calender:
        async with self.pool.acquire() as conn:
            calender: Calender
            query = "SELECT * FROM get_shifts_for_month($1 ,$2)"
            params = [date, user.uid_user]
            calender.shifts = await conn.fetch(query, *params)
            calender.month = date.month
            calender.year = date.year
            return calender

    async def create_shift_member(self, shift: Shift, user: User, wished: bool, assigned: bool):
        async with self.pool.acquire() as conn:
            create_statement = "INSERT INTO shift_member(uid_shift, uid_user, wished, assigned) VALUES ($1, $2, $3, $4)"
            params = [shift.uid_shift, user.uid_user, wished, assigned]
            await conn.execute(create_statement, *params)

    async def update_shift_member(self, shiftmember: ShiftMember):
        async with self.pool.acquire() as conn:
            update_statement = ("UPDATE shift_member SET attendance = $3, wished = $4, assigned = $5"
                                "WHERE uid_shift = $1 AND uid_user = $2")
            params = [shiftmember.uid_shift, shiftmember.uid_user, shiftmember.attendance, shiftmember.wished,
                      shiftmember.assigned]
            await conn.execute(update_statement, *params)

    async def fetch_shift_member(self, shiftmember: ShiftMember):
        async with self.pool.acquire() as conn:
            query = "SELECT * FROM shift_member inner join users WHERE uid_shift = $1 AND uid_user = $2"
            params = [shiftmember.uid_shift, shiftmember.uid_user]
            await conn.execute(query, *params)

    #query should also return information from users, might be time to make some join statements.
    async def fetch_all_shift_members(self, shift: Shift) -> list[ShiftMember]:
        async with self.pool.acquire() as conn:
            query = "SELECT * FROM shift_member inner join users WHERE uid_shift = $1"
            params = [shift.uid_shift]
            result = await conn.execute(query, *params)
            shiftmembers = [ShiftMember(uid_user=member.get('uid_user'),
                                        name=member.get('name'),
                                        email=member.get('email'),
                                        phone=member.get('phone'),
                                        role=member.get('role'),
                                        uid_shift=member.get('uid_shift'),
                                        attendance=member.get('attendance'),
                                        wished=member.get('wished'),
                                        assigned=member.get('assigned')) for member in result]
            return shiftmembers

    async def delete_shift_member(self, shiftmember: ShiftMember):
        async with self.pool.acquire() as conn:
            delete_statement = "DELETE FROM shift_member WHERE uid_shift = $1 AND uid_user = $2"
            params = [shiftmember.uid_shift, shiftmember.uid_user]
            await conn.execute(delete_statement, *params)


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
    # await users_database().create_user(create_user)
    #user = User(name="test", email="<MAIL>", phone="<PHONE>", role="admin", username="test", password="<PASSWORD>")
    #await users_database().delete_user()

    shift = Shift(uid_shift='28926f84-3e64-467c-b207-8a565e2ca386', start_time=datetime.now(), end_time=datetime.now(), active=True)
    # await database.create_shift(shift)


    user_login = UserLogin(username="test", password="<PASSWORD>")
    user = await users_database().fetch_user(user_login)
    await database.create_shift_member(shift, user, False, False)


if __name__ == '__main__':
    asyncio.run(main())
