import datetime

from peewee import *
import uuid

# Database connection
db = PostgresqlDatabase('my_database.db')

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
    uid_user = UUIDField(unique=True) #uuid_generate???
    name = CharField(max_length=255)
    email = CharField(max_length=255, unique=True)
    phone = CharField(max_length=8, unique=True)
    role = ForeignKeyField(clearence_lvl, to_field='role', on_delete='CASCADE')
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
    uid_shift = ForeignKeyField(shifts, to_field='uid_shift', on_delete='CASCADE')
    uid_user = ForeignKeyField(users, to_field='uid_user', on_delete='CASCADE')
    attendance = BooleanField(default=False)
    wished = BooleanField(default=False)
    assigned = BooleanField(default=False)
def create_tables():
    with db:
        db.create_tables([clearence_lvl, users, shifts, shift_member])

# Main execution logic
if __name__ == '__main__':
    create_tables()
    # You can add instances here or perform other database operations
