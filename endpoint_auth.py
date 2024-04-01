from fastapi import APIRouter, Request, HTTPException, Response, status
from fastapi.responses import JSONResponse

from controllers import users_control

from models.auth import Token, UserInfo
from verification import tokenz

from datetime import timedelta

control = users_control.ControllerUsers()


# uvicorn authenticationServer:app --port 8000

# uvicorn authenticationServer:app --port 8000 --ssl-keyfile=localhost-key.pem --ssl-certfile=localhost.pem

router = APIRouter()
expires_in = 60 * 60 * 24 * 7 * 2  # 2 weeks

@router.post("/create-our-token/")
async def create_token_homebrew(response: Response, user = UserInfo):
    # I removed the database connections so it's just for show.
    # Before issuing a token the users credentials should be confirmed in the database

    username = user.user_id
    password = user.password

    ### *** INSERT DATABASE CHECKS *** ###

    # Insert error checks too
    access_token = tokenz.create_access_token()

    response.set_cookie(key="access_token",
                        value=access_token,
                        httponly=True,
                        domain="",  # Note the change here
                        max_age=expires_in,
                        path='/',
                        secure=True,  # Change to False for local testing, True for production
                        samesite="strict")
    return {"created_token": True}


def verify_session_cookie(request: Request):

    session_cookie = request.cookies.get("access_token")

    if not session_cookie:
        raise HTTPException(status_code=401, detail="Session cookie is missing.")

    return UserInfo()

@router.post("/sign-out/")
def sign_out(response: Response):
    # Set the "session" cookie to an empty value and expire it immediately
    response.set_cookie(key="session", value="", expires=0)
    return {"message": "User has been signed out successfully."}


if __name__ == "__main__":
    x = 2
