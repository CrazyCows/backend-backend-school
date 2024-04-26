import asyncio

from src.database.conn_pool import PoolUsersData
from src.models.calender_model import Shift, Calender, ShiftMember
from datetime import date, datetime
from models import db, shifts, shift_member, users, clearence_lvl
from src.models.users_model import User


# This is just an example to show how to use the pool and the database connection - database does not exist yet
# Transactions is used for deletes and inserts to prevent the data from being read when modified.
class Database:
    def __init__(self):
        self.pool = PoolUsersData()
    async def create_shift(self, shift: Shift) -> None:
        # Assuming you have already connected to your database before calling this method
        async with db.atomic_async():
            await shifts.create(
                uid_shift=shift.uid_shift,
                start_time=shift.start_time,
                end_time=shift.end_time,
                active=shift.active,
                creation_date=datetime.now()
            )

    async def update_shift(self, shift: Shift) -> None:
        async with db.atomic_async():
            query = shifts.update(
                start_time=shift.start_time,
                end_time=shift.end_time,
                active=shift.active
            ).where(shifts.uid_shift == shift.uid_shift)
            await db.execute(query)

    async def delete_shift(self, shift: Shift) -> None:
        async with db.atomic_async():
            query = shifts.delete().where(shifts.uid_shift == shift.uid_shift)
            await db.execute(query)

    async def fetch_shift(self, shift: Shift) -> Shift:
        async with db.atomic_async():
            return await shifts.get_or_none(shifts.uid_shift == shift.uid_shift)

    async def fetch_month_shifts(self, date: date, user: User) -> Calender:
        async with db.atomic_async():
            # Assuming get_shifts_for_month() returns shift_id, start_time, end_time, active, myShift
            query = """
                SELECT uid_shift, start_time, end_time, active, myShift
                FROM get_shifts_for_month(?, ?)
            """
            rows = await db.execute_sql(query, (date, user.uid_user))

            shifts = [Shift(
                uid_shift=row[0],
                start_time=row[1],
                end_time=row[2],
                active=row[3],
                myShift=row[4]
            ) for row in rows]

            return Calender(
                shifts=shifts,
                month=date.strftime("%B"),
                year=str(date.year)
            )

    async def create_shift_member(self, shift: Shift, user: User, wished: bool, assigned: bool):
        async with db.atomic_async():
            await shift_member.create(
                uid_shift=shift.uid_shift,
                uid_user=user.uid_user,
                wished=wished,
                assigned=assigned
            )

    async def update_shift_member(self, shiftmember: ShiftMember):
        async with db.atomic_async():
            query = shift_member.update(
                attendance=shiftmember.attendance,
                wished=shiftmember.wished,
                assigned=shiftmember.assigned
            ).where(
                (shift_member.uid_shift == shiftmember.uid_shift) &
                (shift_member.uid_user == shiftmember.uid_user)
            )
            await db.execute(query)

    async def fetch_shift_member(self, shiftmember: ShiftMember):
        async with db.atomic_async():
            return await shift_member.get_or_none(
                (shift_member.uid_shift == shiftmember.uid_shift) &
                (shift_member.uid_user == shiftmember.uid_user)
            )

    async def fetch_all_shift_members(self, shift: Shift) -> list[ShiftMember]:
        async with db.atomic_async():
            return await shift_member.filter(shift_member.uid_shift == shift.uid_shift)

    async def delete_shift_member(self, shiftmember: ShiftMember):
        async with db.atomic_async():
            query = shift_member.delete().where(
                (shift_member.uid_shift == shiftmember.uid_shift) &
                (shift_member.uid_user == shiftmember.uid_user)
            )
            await db.execute(query)

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
