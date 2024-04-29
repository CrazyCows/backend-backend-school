import datetime

from peewee import PostgresqlDatabase
import uuid

# Database connection
db = PostgresqlDatabase(
    "backend_school",
    user="firstuser",
    password="Studyhard1234.",
    host="localhost",
    port=5432,
)

get_shift_for_month_function_query = function_query = """
    CREATE OR REPLACE FUNCTION get_shifts_for_month(month_date DATE, users_id INTEGER) RETURNS TABLE (
       shift_id INT,
       start_time TIMESTAMP,
       end_time TIMESTAMP,
       active BOOLEAN,
       myShift BOOLEAN
    ) AS $$
    BEGIN
       RETURN QUERY
       SELECT shifts.shift_id, shifts.start_time, shifts.end_time, shifts.active,
       CASE WHEN shift_member.user_id = users_id THEN TRUE ELSE FALSE END AS myShift
       FROM shifts JOIN shift_member ON shifts.shift_id = shift_member.shift_id
       WHERE EXTRACT(YEAR FROM shifts.start_time) = EXTRACT(YEAR FROM month_date)
         AND EXTRACT(MONTH FROM shifts.start_time) = EXTRACT(MONTH FROM month_date);
    END;
    $$ LANGUAGE plpgsql;
"""


# Define your base model class from which all tables will inherit
class BaseModel(Model):
    class Meta:
        database = db


class clearence_lvl(BaseModel):
    id = AutoField(primary_key=True)
    uid_clearance = UUIDField(unique=True, null=False, default=uuid.uuid4)
    role = CharField(null=False, max_length=100, unique=True)
    creation_date = DateTimeField(datetime.datetime.now())


# Define a simple User table
class users(BaseModel):
    id = AutoField(primary_key=True)
    uid_user = UUIDField(unique=True)  # uuid_generate???
    name = CharField(max_length=255)
    email = CharField(max_length=255, unique=True)
    phone = CharField(max_length=8, unique=True)
    role = ForeignKeyField(clearence_lvl, to_field="role", on_delete="CASCADE")
    username = CharField(unique=True, max_length=255)
    last_login = DateTimeField(datetime.datetime.now())
    registration = DateTimeField(datetime.datetime.now())
    last_modified = DateTimeField(datetime.datetime.now())
    salt = BinaryUUIDField()
    password = BinaryUUIDField()


class shifts(BaseModel):
    id = AutoField(primary_key=True)
    uid_shift = UUIDField(unique=True)
    start_time = DateTimeField()
    end_time = DateTimeField()
    active = BooleanField()
    creation_date = DateTimeField(datetime.datetime.now())


class shift_member(BaseModel):
    id = AutoField(primary_key=True)
    uid_shift = ForeignKeyField(shifts, to_field="uid_shift", on_delete="CASCADE")
    uid_user = ForeignKeyField(users, to_field="uid_user", on_delete="CASCADE")
    attendance = BooleanField(default=False)
    wished = BooleanField(default=False)
    assigned = BooleanField(default=False)


def create_tables():
    with db:
        db.create_tables([clearence_lvl, users, shifts, shift_member])


def create_function():
    with db:
        db.execute_sql(get_shift_for_month_function_query)


# Main execution logic
if __name__ == "__main__":
    create_tables()
    create_function()
    # You can add instances here or perform other database operations
