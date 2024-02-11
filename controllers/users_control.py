from helpers.singleton import SingletonMeta

# Just an example

# Simply showing a controller
# Note we are using the singleton meta from the helper class to create a singleton pattern
class ControllerUsers(metaclass=SingletonMeta):
    """
    def __init__(self):
        self.db_psql_users = auth_db.Database()

    async def create_user(self, user_id, user_email):
        try:
            is_created = await self.db_psql_users.create_user(user_id, user_email)
            if is_created:
                return "Success"

        except Exception as e:
            raise Exception(f"Error creating user: {e}")

    async def delete_user(self, user_id):
        try:
            is_deleted = await self.db_psql_users.delete_user(user_id)
            if is_deleted:
                return "Success"

        except Exception as e:
            raise Exception(f"Error deleting user: {e}")
    """