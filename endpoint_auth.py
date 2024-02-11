from fastapi import APIRouter, Request, HTTPException, Response, status
from fastapi.responses import JSONResponse

from controllers import users_control

from firebase_admin import credentials, initialize_app, auth
from models.auth import Token, UserInfo
from verification import tokenz

from datetime import timedelta

control = users_control.ControllerUsers()

# Initialize the Firebase Admin SDK
cred = credentials.Certificate("C:/Users/emils/Downloads/minlov-firebase-adminsdk-tcvpw-6ef6458d5d.json")
initialize_app(cred)


# uvicorn authenticationServer:app --port 8000

# uvicorn authenticationServer:app --port 8000 --ssl-keyfile=localhost-key.pem --ssl-certfile=localhost.pem

router = APIRouter()
expires_in = 60 * 60 * 24 * 7 * 2  # 2 weeks

@router.post("/create-our-token/")
async def create_token_homebrew(response: Response):
    # I removed the database connections so it's just for show.
    # Before issuing a token the users credentials should be confirmed in the database

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

# Google auth
# Gauth sends a token upon requesting firebase but its not a session cookie. it changes every hour thus we are creating our own
@router.post("/create-google-token/")
async def create_token(token: Token, response: Response):
    """Exchanges a Firebase ID token for a session cookie and sets it as HttpOnly."""
    try:
        decoded_token = auth.verify_id_token(token.token)
        session_cookie = auth.create_session_cookie(token.token, expires_in=expires_in)
        await control.create_user(decoded_token['uid'], decoded_token.get('email', None))
        response.set_cookie(key="session", value=session_cookie, max_age=expires_in, secure=True, samesite='strict', httponly=True)
        return {"message": "Session cookie set successfully."}
    except auth.RevokedIdTokenError:
        raise HTTPException(status_code=401, detail="ID token has been revoked. Ask user to re-authenticate.")
    except auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="ID token is invalid. Ask user to sign in again.")

@router.post("/check-login/")
def check_token(request: Request):

    session_cookie = request.cookies.get("session")

    if not session_cookie:
        raise HTTPException(status_code=401, detail="Session cookie is missing.")

    try:
        auth.verify_session_cookie(session_cookie, check_revoked=True)
        return JSONResponse(status_code=200, content={"authenticated": True})
    except auth.InvalidSessionCookieError:
        raise HTTPException(status_code=401, detail="Session cookie is invalid.")


def verify_session_cookie(request: Request):

    session_cookie = request.cookies.get("session")

    if not session_cookie:
        raise HTTPException(status_code=401, detail="Session cookie is missing.")

    try:
        decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)
        uid = decoded_claims.get('uid')
        email = decoded_claims.get('email', None)
        return UserInfo(user_id=uid, email=email)
    except auth.InvalidSessionCookieError:
        raise HTTPException(status_code=401, detail="Session cookie is invalid.")


@router.post("/sign-out/")
def sign_out(response: Response):
    # Set the "session" cookie to an empty value and expire it immediately
    response.set_cookie(key="session", value="", expires=0)
    return {"message": "User has been signed out successfully."}


if __name__ == "__main__":
    x = 2
