from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, text, UUID, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from src.database.conn_pool import get_db_session, engine
import uuid
from datetime import datetime

Base = declarative_base()

def create_ossp_extension():
    with get_db_session() as session:
        sql_command = text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")
        session.execute(sql_command)
        session.commit()

class ClearanceLevelORM(Base):
    __tablename__ = "clearance_levels"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid_user: Column[UUID] = Column(UUID(as_uuid=True), primary_key=True,
                                     server_default=func.uuid_generate_v4())
    role = Column(String(100), unique=True, nullable=False)
    creation_date = Column(DateTime, default=datetime.now)


class UserORM(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid_user = Column(UUID(as_uuid=True), unique=True, server_default=func.uuid_generate_v4())
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(64), unique=True, nullable=False)
    role = Column(String, ForeignKey("clearance_levels.role"), nullable=False)
    username = Column(String(255), unique=True)
    last_login = Column(DateTime, default=datetime.now)
    registration = Column(DateTime, default=datetime.now)
    last_modified = Column(DateTime, default=datetime.now)
    password = Column(String, nullable=False)
    role_relationship = relationship("ClearanceLevelORM")


class ShiftORM(Base):
    __tablename__ = "shifts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid_shift = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    active = Column(Boolean, default=True)
    creation_date = Column(DateTime, default=datetime.now)

class ShiftMemberORM(Base):
    __tablename__ = "shift_members"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid_shift = Column(UUID(as_uuid=True), ForeignKey("shifts.uid_shift"), nullable=False)
    uid_user = Column(UUID(as_uuid=True), ForeignKey("users.uid_user"), nullable=False)
    attendance = Column(Boolean, default=False)
    wished = Column(Boolean, default=False)
    assigned = Column(Boolean, default=False)
    shift = relationship("ShiftORM")
    user = relationship("UserORM")


def create_function():
    function_sql = text("""
    CREATE OR REPLACE FUNCTION get_shifts_for_month(month_date DATE, uid_user UUID) RETURNS TABLE (
       shift_id INT,
       start_time TIMESTAMP,
       end_time TIMESTAMP,
       active BOOLEAN,
       myShift BOOLEAN
    ) AS $$
    BEGIN
       RETURN QUERY
       SELECT shifts.uid_shift, shifts.start_time, shifts.end_time, shifts.active,
       CASE WHEN shift_members.uid_user = uid_user THEN TRUE ELSE FALSE END AS myShift
       FROM shifts JOIN shift_members ON shifts.uid_shift = shift_members.uid_shift
       WHERE EXTRACT(YEAR FROM shifts.start_time) = EXTRACT(YEAR FROM month_date)
         AND EXTRACT(MONTH FROM shifts.start_time) = EXTRACT(MONTH FROM month_date);
    END;
    $$ LANGUAGE plpgsql;
    """)

    with get_db_session() as active_session:
        active_session.execute(function_sql)
        active_session.commit()


if __name__ == "__main__":
    create_ossp_extension()
    Base.metadata.create_all(engine)
    create_function()
