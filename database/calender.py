from database.conn_pool import PoolUsersData
from models.calender_model import Shift, Calender

# This is just an example to show how to use the pool and the database connection - database does not exist yet
# Transactions is used for deletes and inserts to prevent the data from being read when modified.
class Database:
    def __init__(self):
        self.pool = PoolUsersData()

    async def create_shift(self, shift: Shift):
        async with self.pool.acquire() as conn:
            try:
                create_statement = "INSERT INTO shifts(start_time, end_time, active) VALUES ($1, $2, $3)"
                params = [shift.start_time, shift.end_time, shift.active]
                await conn.execute(create_statement, *params)
            except Exception as e:
                print("define a proper exception")
                print(e)

    async def delete_shift(self, shift: Shift):
        async with self.pool.acquire() as conn:
            try:
                query = "DELETE FROM shifts WHERE shifts.shift_id=$1"
                params = shift.uid_shift
                await conn.execute(query, params)
            except Exception as e:
                print("define propper exception")
                print(e)


    async def fetch_shift(self, shift: Shift, period) -> Shift:
        async with self.pool.acquire() as conn:
            try:
                query = "SELECT * FROM shifts WHERE active=TRUE"
                results = await conn.fetch(query)

            except Exception as e:
                print("define propper exception")
                print(e)

    async def fetch_month_shifts(self, calender: Calender) -> Calender:
        raise NotImplementedError("hallo mand!! kom lige igang med at få mig implemnteret")

