from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from models.users_model import User, UserLogin, CreateUser
from models.calender_model import Shift
from controllers import simple_controller
from datetime import date

# Just an example of how to setup routing for CRUD

router = APIRouter()
controls = simple_controller.Controller()

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
        await controls.get_all_users()
        return JSONResponse(content={"successfully fetched all users", 200})
    except:
        return JSONResponse(content={"not successful deleting user", 403})

@router.post("/creat-shift/")
async def create_shift(shift: Depends(Shift)):
    try:
        await controls.create_shift(shift)
        return JSONResponse(content={"successfully created shift", 200})
    except:
        return JSONResponse(content={"not successful creating shift", 403})

@router.get("/fetch-shift/")
async def fetch_shift(shift: Depends(Shift)):
    try:
        await controls.get_shift(shift)
        return JSONResponse(content={"successfully fetched shift", 200})
    except:
        return JSONResponse(content={"not successful fetching shift", 403})

@router.get("/fetch-shifts-for-month/")
async def fetch_all_users(date: Depends(date), user: Depends(User)):
    try:
        await controls.get_shifts_for_month(date, user)
        return JSONResponse(content={"successfully fetched all shifts for month", 200})
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