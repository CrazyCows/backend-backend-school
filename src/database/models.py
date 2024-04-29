from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from src.database.conn_pool import get_db_session, engine
import uuid
import datetime

Base = declarative_base()


class ClearanceLevel(Base):
    __tablename__ = "clearance_levels"
    id = Column(Integer, primary_key=True)
    uid_clearance = Column(String, unique=True, default=lambda: str(uuid.uuid4()))
    role = Column(String(100), unique=True, nullable=False)
    creation_date = Column(DateTime, default=datetime.datetime.now)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    uid_user = Column(String, unique=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(8), unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey("clearance_levels.id"), nullable=False)
    username = Column(String(255), unique=True)
    last_login = Column(DateTime, default=datetime.datetime.now)
    registration = Column(DateTime, default=datetime.datetime.now)
    last_modified = Column(DateTime, default=datetime.datetime.now)
    salt = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = relationship("ClearanceLevel")


class Shift(Base):
    __tablename__ = "shifts"
    id = Column(Integer, primary_key=True)
    uid_shift = Column(String, unique=True, default=lambda: str(uuid.uuid4()))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    active = Column(Boolean, default=True)
    creation_date = Column(DateTime, default=datetime.datetime.now)


class ShiftMember(Base):
    __tablename__ = "shift_members"
    id = Column(Integer, primary_key=True)
    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    attendance = Column(Boolean, default=False)
    wished = Column(Boolean, default=False)
    assigned = Column(Boolean, default=False)
    shift = relationship("Shift")
    user = relationship("User")


def create_function(session):
    function_sql = text("""
    CREATE OR REPLACE FUNCTION get_shifts_for_month(month_date DATE, users_id INTEGER) RETURNS TABLE (
       shift_id INT,
       start_time TIMESTAMP,
       end_time TIMESTAMP,
       active BOOLEAN,
       myShift BOOLEAN
    ) AS $$
    BEGIN
       RETURN QUERY
       SELECT shifts.id, shifts.start_time, shifts.end_time, shifts.active,
       CASE WHEN shift_members.user_id = users_id THEN TRUE ELSE FALSE END AS myShift
       FROM shifts JOIN shift_members ON shifts.id = shift_members.shift_id
       WHERE EXTRACT(YEAR FROM shifts.start_time) = EXTRACT(YEAR FROM month_date)
         AND EXTRACT(MONTH FROM shifts.start_time) = EXTRACT(MONTH FROM month_date);
    END;
    $$ LANGUAGE plpgsql;
    """)

    with session as active_session:
        active_session.execute(function_sql)
        active_session.commit()


if __name__ == "__main__":
    session = get_db_session()
    Base.metadata.create_all(engine)
    create_function(session)
