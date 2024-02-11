from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.conn_pool import PoolUsersData, BasePool
from endpoint_auth import router as auth
from endpoint_profile import router as profile
from controllers import users_control
from contextlib import asynccontextmanager

# This starts the app and adds the routers to it
app = FastAPI()

# Allows connections from specific endpoints. Is required to connect from a browser
origins = [
    'Insert your local vite-servers ip here -  I will setup the vite server for u...',
]

# Cors middleware - it allows for setting cookies in browser
# Long story short browsers have a lot of security which rely on CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


# Instantiate things here...
@asynccontextmanager
async def startup_event():
    await PoolUsersData().initialize_pool()
    users_control.ControllerUsers()


app.include_router(auth, prefix="/auth")
app.include_router(profile, prefix="/profile")

