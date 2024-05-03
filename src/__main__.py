from contextlib import (
    asynccontextmanager,
)

import uvicorn
import src.database.users
from src.database.models import create_db
from src.database.users import create_clearence_level_sync, create_user_sync
from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware,
)

from src.dto.users_model import CreateUser
from src.endpoint_profile import (
    router as profile,
)
import asyncio
import sys

sys.path.insert(0, '/Users/emil/belief_revision_engine/backend-backend-school')

# This starts the app and adds the routers to it
app = FastAPI()

# Allows connections from specific endpoints. Is required to connect from a browser
origins = [
    # "http://localhost:63342",
    # "http://localhost",
    # "http://127.0.0.1",
    # "https://localhost",
    # "https://127.0.0.1"
    "https://wfvagtplan.dk",
    "https://www.wfvagtplan.dk"
]

# Cors middleware - it allows for setting cookies in browser
# Long story short browsers have a lot of security which rely on CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(profile, prefix="")


def server_start():
    try:
        create_db()
        create_clearence_level_sync("admin")
        create_clearence_level_sync("dev")
        create_clearence_level_sync("coworker")
        createuser = CreateUser(name="John Doe", email="john@doe.com", phone="87654321", role="admin", username="john", password="t")
        create_user_sync(createuser)
    except:
        print("Failed to create clearence level")

server_start()


# TODO: Create a function for creating tables and database upon start. Only if they don't exists.
if __name__ == "__main__":
    # create_db()
    # Example user data
    # create_clearence_level_sync("admin")
    # createuser = CreateUser(name="John Doe", email="john@doe.com", phone="87654321", role="admin", username="john", password="ZEUvE2zTFB")
    # Example database operations
    # create_user_sync(createuser)
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    """"""
