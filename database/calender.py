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

    async def create_shift(self, shift: Shift) -> None:
        async with self.pool.acquire() as conn:
            create_statement = "INSERT INTO shifts(start_time, end_time, active, creation_date) VALUES ($1, $2, $3, $4)"
            params = [shift.start_time, shift.end_time, shift.active, datetime.now()]
            await conn.execute(create_statement, *params)

    async def update_shift(self, shift: Shift) -> None:
        async with self.pool.acquire() as conn:
            update_statement = ("UPDATE shifts SET start_time = $2, end_time = $3, "
                                "active = $4 WHERE uid_shift = $1")
            params = [shift.uid_shift, shift.start_time, shift.end_time, shift.active]
            await conn.execute(update_statement, *params)


    async def delete_shift(self, shift: Shift) -> None:
        async with self.pool.acquire() as conn:
            query = "DELETE FROM shifts WHERE shifts.uid_shift = $1"
            params = shift.uid_shift
            await conn.execute(query, params)

    async def fetch_shift(self, shift: Shift) -> Shift:
        async with self.pool.acquire() as conn:
            query = "SELECT * FROM shifts WHERE uid_shift = $1"
            params = shift.uid_shift
            results = await conn.fetch(query, params)
            return results

    # TODO: This can't be right(?)
    # It's not :(( I have checked the functions above, and they should be working now. Down under hasn't been tested properly, and fetch_month doesn't work yet
    async def fetch_month_shifts(self, date: date, user: User) -> Calender:
        async with self.pool.acquire() as conn:
            query = "SELECT * FROM get_shifts_for_month($1, $2)"
            params = [date, user.uid_user]
            rows = await conn.fetch(query, *params)
            shifts = [Shift(
                uid_shift=row['uid_shift'],
                start_time=row['start_time'],
                end_time=row['end_time'],
                active=row['active'],
                description=row.get('my_shift')  # Assuming 'my_shift' is intended to map to 'description'
            ) for row in rows]

            return Calender(
                shifts=shifts,
                month=date.strftime("%B"),
                year=str(date.year)
            )


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

    member1 = ShiftMember(uid_user="c277b223-cd1f-482f-91ee-9622472c1d79", name="test")
    member2 = ShiftMember(uid_user="c277b223-cd1f-482f-91ee-9622472c1d79", name="test")

    dummy_shift = Shift(
        uid_shift="3bbfc38e-ed04-45fb-87cc-c049bf8ec96c",
        start_time=datetime(2024, 4, 20, 8, 0),  # April 20, 2024, 8:00 AM
        end_time=datetime(2024, 4, 20, 16, 0),  # April 20, 2024, 4:00 PM
        wished_shift_members=[member1, member2],
        actual_shift_members=[member1],
        active=True,
        description="Morning shift"
    )
    print(dummy_shift)

    await database.create_shift(dummy_shift)

    # Create a dummy user object
    test_user = User(uid_user="c277b223-cd1f-482f-91ee-9622472c1d79")

    # Assume asyncpg pool creation and date object
    test_date = date(2024, 4, 1)
    single_shift = await database.fetch_shift(dummy_shift)
    print(single_shift)
    print("--------")
    calender = await database.fetch_month_shifts(test_date, test_user)
    print(calender)


if __name__ == '__main__':
    asyncio.run(main())
