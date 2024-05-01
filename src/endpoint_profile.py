from fastapi import (
    APIRouter,
    Request,
    Response,
    HTTPException,
)
from fastapi.responses import (
    JSONResponse,
)
from pydantic import BaseModel

from src.database.users import create_clearence_level_sync, create_user_sync
from src.dto.users_model import (
    User,
    UserLogin,
    CreateUser,
)
from src.dto.calender_model import (
    Shift,
)
from src.controllers import (
    simple_controller,
)
from datetime import date
from cryptography.fernet import Fernet
from loguru import logger
# Just an example of how to setup routing for CRUD

router = APIRouter()
controls = simple_controller.Controller()
key = Fernet.generate_key()
cipher = Fernet(key)
max_age = 3600


def encrypt_data(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()


def decrypt_data(data: str) -> str:
    return cipher.decrypt(data.encode()).decode()


def get_cookie(request: Request):
    encrypted_data = request.cookies.get("secure_cookie")
    if encrypted_data:
        decrypted_data = decrypt_data(encrypted_data)
        return decrypted_data  # Should be userId (for the love of god)
    raise HTTPException(status_code=403)


async def is_user_admin(
    request: Request,
):
    uid_user = get_cookie(request)
    user = User(uid_user=uid_user)
    user = await controls.check_user_active(user)
    if user.role != "admin":
        raise HTTPException(status_code=403)


# TODO: Discuss if this should return
@router.post("/create-user/")
async def create_user(user: CreateUser, request: Request):
    await is_user_admin(request)
    try:
        await controls.create_user(user)
        return JSONResponse(
            content={"message": "successfully created user"},
            status_code=201,
        )
    except:
        return JSONResponse(
            content={"message": "not successful creating user"},
            status_code=403,
        )


@router.post("/user-login/")
async def user_login(user: UserLogin):
    try:
        current_user = await controls.login(user)
        data = current_user.uid_user
        encrypted_data = encrypt_data(data)

        response = JSONResponse(
            content={"message": "successfully logged in user", "data": current_user.dict()},
            status_code=200,
        )
        response.set_cookie(
            key="secure_cookie",
            value=encrypted_data,
            max_age=max_age,
            httponly=True,
            samesite="none",
            secure=True
        )
        return response
    except:
        return JSONResponse(
            content={"message": "not successful logging in user"},
            status_code=403,
        )


# TODO: Rewrite such it only takes in a cookie as argument and passes the UID for the user to delete a given user to improve security.
@router.delete("/delete-user/")
async def delete_user(user: User, request: Request):
    await is_user_admin(request)
    try:
        await controls.delete_user(user)
        return JSONResponse(
            content={"message": "successfully deleted user"},
            status_code=200,
        )
    except:
        return JSONResponse(
            content={"message": "not successful deleting user"},
            status_code=403,
        )


@router.get("/fetch-all-users/")
async def fetch_all_users(
    request: Request,
):
    get_cookie(request)
    try:
        all_users = await controls.fetch_all_users()
        all_users = [user.dict() for user in all_users]
        return JSONResponse(
            content={
                "message": "successfully fetched all users",
                "all_users": all_users,
            },
            status_code=200,
        )
    except:
        return JSONResponse(
            content={"message": "not successful deleting user"},
            status_code=403,
        )


@router.post("/create-shift/")
async def create_shift(shift: Shift, request: Request):
    await is_user_admin(request)
    try:
        await controls.create_shift(shift)
        return JSONResponse(
            content={"message": "successfully created shift"},
            status_code=200,
        )
    except:
        return JSONResponse(
            content={"message": "not successful creating shift"},
            status_code=403,
        )


@router.get("/fetch-shift/")
async def fetch_shift(shift: Shift, request: Request):
    get_cookie(request)
    try:
        _shift = await controls.get_shift(shift)
        return JSONResponse(
            content={
                "message": "Successfully fetched shift",
                "shift": _shift.dict(),
            },
            status_code=200,
        )
    except:
        return JSONResponse(
            content={"message": "not successful fetching shift"},
            status_code=403,
        )


class ShiftRequest(BaseModel):
    chosen_date: date  # Ensure the type and field name are correct


@router.post("/fetch-shifts-for-month/")
async def fetch_shifts_for_month(
    chosen_date: ShiftRequest,
    request: Request,
):

    logger.info(f"fetch shifts for: {request.cookies}")
    chosen_date = chosen_date.chosen_date
    uid_user = get_cookie(request)
    user = User(uid_user=uid_user)
    try:
        print("hi")
        month_calender = await controls.get_shifts_for_month(chosen_date)
        print("hi")
        return JSONResponse(
            content={
                "message": "successfully fetched all shifts for month",
                "shifts": month_calender.dict(),
            },
            status_code=200,
        )
    except:
        return JSONResponse(
            content={"message": "not successful fetching all shifts for month"},
            status_code=400,
        )


@router.delete("/delete-shift/")
async def delete_shift(shift: Shift, request: Request):
    await is_user_admin(request)
    try:
        await controls.delete_shift(shift)
        return JSONResponse(
            content={"message": "successfully deleted shift"},
            status_code=200,
        )
    except:
        return JSONResponse(
            content={"message": "not successful deleting shift"},
            status_code=403,
        )


@router.options("/hi/")
async def test_options():
    return
