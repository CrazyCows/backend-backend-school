import asyncio
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.sql import func
from src.dto.calender_model import Shift, ShiftMember, ShiftRequest  # Ensure these are SQLAlchemy ORM models
from src.database.models import ShiftORM, ShiftMemberORM
from src.dto.users_model import User
from src.conf.settings import settings
from src.database.conn_pool import get_async_db_session


async def create_shift(shift: Shift) -> None:
    shift_orm = ShiftORM(start_time=shift.start_time, end_time=shift.end_time)
    async with get_async_db_session() as session:
        session.add(shift_orm)
        await session.commit()


async def update_shift(shift: Shift) -> None:
    async with get_async_db_session() as session:
        stmt = select(ShiftORM).where(ShiftORM.uid_shift == shift.uid_shift)
        result = await session.execute(stmt)
        db_shift = result.scalar().first()
        if db_shift:
            db_shift.start_time = shift.start_time
            db_shift.end_time = shift.end_time
            db_shift.uid_shift = shift.uid_shift
            db_shift.active = shift.active
            await session.commit()


async def delete_shift(shift: Shift) -> None:
    async with get_async_db_session() as session:
        stmt = select(ShiftORM).where(ShiftORM.uid_shift == shift.uid_shift)
        result = await session.execute(stmt)
        db_shift = result.scalars().first()
        if db_shift:
            await session.delete(db_shift)
            await session.commit()


async def fetch_shift(shift: Shift) -> Shift:
    shift_id = shift.uid_shift
    async with get_async_db_session() as session:
        result = await session.execute(select(ShiftORM).where(ShiftORM.uid_shift == shift_id))
        return result.scalars().first()


async def fetch_month_shifts(shift_request: ShiftRequest) -> list[Shift]:
    print("hi")
    print(shift_request)
    _date = shift_request.chosen_date
    print("hi")
    month = _date.month
    print("hi")
    year = _date.year
    print(month, year)
    print("hi")
    async with get_async_db_session() as session:
        stmt = select(ShiftORM).where(
            func.extract('month', ShiftORM.start_time) == month,
            func.extract('year', ShiftORM.start_time) == year
        )
        result = await session.execute(stmt)
        shifts = result.scalars().all()
        return [Shift(uid_shift=str(s.uid_shift), start_time=s.start_time, end_time=s.end_time, active=s.active) for s in shifts]


"""
    __tablename__ = "shift_members"
    id = Column(Integer, primary_key=True)
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    attendance = Column(Boolean, default=False)
    wished = Column(Boolean, default=False)
    assigned = Column(Boolean, default=False)
    shift = relationship("ShiftORM")
    user = relationship("UserORM")
"""


async def create_shift_member(shift_member: ShiftMember):
    shift_member_orm = ShiftMemberORM(uid_user=shift_member.uid_user,
                                      attendance=shift_member.attendance,
                                      wished=shift_member.wished,
                                      assigned=shift_member.assigned,
                                      uid_shift=shift_member.uid_shift)
    async with get_async_db_session() as session:
        session.add(shift_member_orm)
        await session.commit()


async def fetch_shift_member(shift_member: ShiftMember) -> ShiftMember:
    shift_id = shift_member.uid_shift
    user_id = shift_member.uid_user
    async with get_async_db_session() as session:
        stmt = select(ShiftMemberORM).where(ShiftMemberORM.uid_shift == shift_id, ShiftMemberORM.uid_user == user_id)
        result = await session.execute(stmt)
        db_shift_member = result.scalars().first()
        if db_shift_member:
            return ShiftMember(uid_shift=db_shift_member.uid_shift,
                               uid_user=db_shift_member.uid_user,
                               attendance=db_shift_member.attendance,
                               wished=db_shift_member.wished,
                               assigned=db_shift_member.assigned)
        else:
            raise Exception("No such shift member")



async def fetch_all_shift_members(shift: Shift) -> list[ShiftMember]:
    async with get_async_db_session() as session:
        stmt = select(ShiftMemberORM).where(ShiftMemberORM.uid_shift == shift.uid_shift)
        result = await session.execute(stmt)
        result_list = result.scalars().all()
        return_list = []
        for shift_member in result_list:
            return_list.append(ShiftMember(
                uid_shift=shift_member.uid_shift,
                uid_user=shift_member.uid_user,
                name = shift_member.name,
                email = shift_member.email,
                phone = shift_member.phone,
                role = shift_member.role,
                attendance = shift_member.attendance,
                wished = shift_member.wished,
                assigned = shift_member.assigned,
            ))
        return return_list


async def delete_shift_member(shift_member: ShiftMember):
    async with get_async_db_session() as session:
        stmt = select(ShiftMemberORM).where(ShiftMemberORM.uid_user == shift_member.uid_user)
        result = await session.execute(stmt)
        db_shift_member = result.scalars().first()
        if db_shift_member:
            await session.delete(db_shift_member)
            await session.commit()

async def update_shift_member(shift_member: ShiftMember):
    async with get_async_db_session() as session:
        stmt = select(ShiftMemberORM).where(ShiftMemberORM.uid_shift == shift_member.uid_shift and ShiftMemberORM.uid_user == shift_member.uid_user)
        result = await session.execute(stmt)
        db_shift_member = result.scalars().first()
        if db_shift_member:
            db_shift_member.uid_shift = shift_member.uid_shift
            db_shift_member.uid_user = shift_member.uid_user
            db_shift_member.attendance = shift_member.attendance
            db_shift_member.wished = shift_member.wished
            db_shift_member.assigned = shift_member.assigned
            await session.commit()


async def main():
    # Create a dummy user
    user = User(uid_user="c27507bd-41a8-4d7b-b6a1-6b4c62b6935e", name="test2")

    # Create a dummy shift
    shift = Shift(
        uid_shift="6db795a6-2e92-42a8-9991-0a5c4320dba7",
        start_time=datetime(2024, 4, 20, 8, 0),  # April 20, 2024, 8:00 AM
        end_time=datetime(2024, 4, 20, 16, 0),  # April 20, 2024, 4:00 PM
        active=True,
        description="Morning shift",
        user_id=user.uid_user  # Assume relationship defined in models
    )

    # Create a dummy shift member

    shift_member = ShiftMember(uid_user="c27507bd-41a8-4d7b-b6a1-6b4c62b6935e",
                               uid_shift="6db795a6-2e92-42a8-9991-0a5c4320dba7")

    #await create_shift(shift)
    #values = await fetch_month_shifts(datetime.now())
    #await create_shift_member(shift_member)
    #shiftmember = await fetch_shift_member(shift_member.uid_shift, shift_member.uid_user)
    #await delete_shift_member(shift_member)
    await delete_shift(shift)
    print("-------------- result --------------")
    #print(shiftmember.uid_shift)
    """
    # Fetch the shift
    fetched_shift = await fetch_shift(shift.uid_shift)
    print("Fetched Shift:", fetched_shift)
    
    # Update the shift (e.g., change active status)
    shift.active = False
    await update_shift(shift)
    
    # Fetch and print month shifts
    calendar_shifts = await fetch_month_shifts(date(2024, 4, 1), user.uid_user)
    print("Shifts in April 2024:", calendar_shifts)
    """


if __name__ == '__main__':
    asyncio.run(main())
