import asyncio
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.sql import func
from src.dto.calender_model import Shift, ShiftMember  # Ensure these are SQLAlchemy ORM models
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
        await session.execute(
            update(ShiftORM)
            .where(ShiftORM.uid_shift == shift.uid_shift)
            .values(start_time=shift.start_time, end_time=shift.end_time, active=shift.active)
        )
        await session.commit()

async def delete_shift(shift: Shift) -> None:
    shift_orm = ShiftORM(uid_shift=shift.uid_shift)
    async with get_async_db_session() as session:
        await session.delete(shift).where(shift.uid_shift == shift.uid_shift)
        await session.commit()

async def fetch_shift(shift_id: str) -> Shift:
    async with get_async_db_session() as session:
        result = await session.execute(select(ShiftORM).where(ShiftORM.uid_shift == shift_id))
        return result.scalars().first()

async def fetch_month_shifts(date: datetime.date) -> list:
    async with get_async_db_session() as session:
        stmt = select(ShiftORM).where(
            func.extract('month', ShiftORM.start_time) == date.month,
            func.extract('year', ShiftORM.start_time) == date.year
        )
        result = await session.execute(stmt)
        return result.scalars().all()
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
    shift_member_orm = ShiftMemberORM(user_id=shift_member.user_id,
                                      attendance=shift_member.attendance,
                                      wished=shift_member.wished,
                                      assigned=shift_member.assigned,
                                      shift_id=shift_member.shift_id)
    async with get_async_db_session() as session:
        session.add(shift_member_orm)
        await session.commit()

async def fetch_shift_member(shift_id: str, user_id: str) -> ShiftMember:
    async with get_async_db_session() as session:
        result = await session.execute(
            select(ShiftMember)
            .where(ShiftMember.uid_shift == shift_id, ShiftMember.uid_user == user_id)
        )
        return result.scalars().first()

async def delete_shift_member(shift_member: ShiftMember):
    async with get_async_db_session() as session:
        await session.delete(shift_member)
        await session.commit()

async def main():
    # Create a dummy user
    user = User(uid_user="c277b223-cd1f-482f-91ee-9622472c1d79", name="John Doe")

    
    # Create a dummy shift
    shift = Shift(
        uid_shift="3bbfc38e-ed04-45fb-87cc-c049bf8ec96c",
        start_time=datetime(2024, 4, 20, 8, 0),  # April 20, 2024, 8:00 AM
        end_time=datetime(2024, 4, 20, 16, 0),   # April 20, 2024, 4:00 PM
        active=True,
        description="Morning shift",
        user_id=user.uid_user  # Assume relationship defined in models
    )


    # shift_member = ShiftMember(uid_user=)
    
    await create_shift(shift)
    values = await fetch_month_shifts(datetime.now())
    #await create_shift_member()
    #await fetch_shift_member()
    #await delete_shift_member(shift)
    #await delete_shift(shift)
    print(values)
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