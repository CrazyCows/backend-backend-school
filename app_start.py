from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.conn_pool import PoolUsersData
from endpoint_profile import router as profile
from contextlib import asynccontextmanager

# This starts the app and adds the routers to it
app = FastAPI()

# Allows connections from specific endpoints. Is required to connect from a browser
origins = [
    "http://localhost:63342",  # Assuming you're using http and not https
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



@app.on_event("startup")
async def startup_event():
    await PoolUsersData().initialize_pool()


app.include_router(profile, prefix="")

