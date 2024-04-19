from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from models.users_model import User, UserLogin, CreateUser
from models.calender_model import Shift
from controllers import simple_controller
from datetime import date

# Just an example of how to setup routing for CRUD

router = APIRouter()
controls = simple_controller.Controller()

# TODO: Discuss if this should return
@router.post("/create-user/")
async def create_user(user: Depends(CreateUser)):
    try:
        await controls.create_user(user)
        return JSONResponse(content={"successfully created user", 200})
    except:
        return JSONResponse(content={"not successful creating user", 403})


@router.get("/fetch-user/")
async def fetch_user(user: Depends(UserLogin)):
    try:
        await controls.login(user)
        return JSONResponse(content={"successfully logged in user", 200})
    except:
        return JSONResponse(content={"not successful logging in user", 403})

# TODO: Rewrite such it only takes in a cookie as argument and passes the UID for the user to delete a given user to improve security.
@router.delete("/delete-user/")
async def delete_user(user: Depends(User)):
    try:
        await controls.delete_user(user)
        return JSONResponse(content={"successfully deleted user", 200})
    except:
        return JSONResponse(content={"not successful deleting user", 403})

@router.get("/fetch-all-users/")
async def fetch_all_users():
    try:
        all_users = await controls.fetch_all_users()
        all_users = [user.dict() for user in all_users]
        return JSONResponse(content={"message": "successfully fetched all users", 'all_users': all_users}, status_code=200)
    except:
        return JSONResponse(content={"not successful deleting user", 403})

@router.post("/create-shift/")
async def create_shift(shift: Shift = Depends(Shift)):
    try:
        await controls.create_shift(shift)
        return JSONResponse(content={"successfully created shift", 200})
    except:
        return JSONResponse(content={"not successful creating shift", 403})

@router.get("/fetch-shift/")
async def fetch_shift(shift: Shift = Depends(Shift)):
    try:
        _shift = await controls.get_shift(shift)
        return JSONResponse(content={"message": "Successfully fetched shift", "shift": _shift.dict()}, status_code=200)
    except:
        return JSONResponse(content={"not successful fetching shift", 403})

@router.get("/fetch-shifts-for-month/")
async def fetch_shifts_for_month(date: Depends(date), user: Depends(User)):
    try:
        month_shifts = await controls.get_shifts_for_month(date, user)
        return JSONResponse(content={"message": "successfully fetched all shifts for month", "shifts": month_shifts.dict()}, status_code=200)
    except:
        return JSONResponse(content={"not successful fetching all shifts for month", 403})

@router.delete("/delete-shift/")
async def delete_shift(shift: Depends(Shift)):
    try:
        await controls.delete_shift(shift)
        return JSONResponse(content={"successfully deleted shift", 200})
    except:
        return JSONResponse(content={"not successful deleting shift", 403})

@router.options("/hi/")
async def test_options():
    return