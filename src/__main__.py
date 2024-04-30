from contextlib import (
    asynccontextmanager,
)

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware,
)
from src.endpoint_profile import (
    router as profile,
)
import sys

sys.path.insert(0, '/Users/emil/belief_revision_engine/backend-backend-school')



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
    expose_headers=["*"],
)

app.include_router(profile, prefix="")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
