from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from models.users_model import User, UserLogin, CreateUser
from models.calender_model import Shift
from controllers import simple_controller
from datetime import date
from cryptography.fernet import Fernet

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
    print("getting encrypted cookie")
    encrypted_data = request.cookies.get("secure_cookie")
    print(encrypted_data)
    print("got encrypted cookie")
    if encrypted_data:
        decrypted_data = decrypt_data(encrypted_data)
        print(decrypted_data)
        print("should be uid")
        return decrypted_data # Should be userId (for the love of god)
    raise HTTPException(status_code=403)

async def is_user_admin(request: Request):
    print("getcookie yes?")
    uid_user = get_cookie(request)
    print(uid_user)
    print("getcookie works:)")
    user = User(uid_user=uid_user)
    user = await controls.check_user_active(user)
    if user.role != "admin":
        raise HTTPException(status_code=403)

# TODO: Discuss if this should return
@router.post("/create-user/")
async def create_user(user: CreateUser, request: Request):
    print("is admin ----------")
    await is_user_admin(request)
    print("admin ok ----------")
    try:
        await controls.create_user(user)
        return JSONResponse(content={"message": "successfully created user"}, status_code=201)
    except:
        return JSONResponse(content={"message": "not successful creating user"}, status_code=403)


@router.post("/user-login/")
async def user_login(user: UserLogin, response: Response):
    try:
        current_user = await controls.login(user)
        data = current_user.uid_user
        encrypted_data = encrypt_data(data)
        response = JSONResponse(content={"message": "successfully logged in user"}, status_code=200)
        response.set_cookie(key="secure_cookie", value=encrypted_data, max_age=max_age)
        return response
    except:
        return JSONResponse(content={"message": "not successful logging in user"}, status_code=403)

# TODO: Rewrite such it only takes in a cookie as argument and passes the UID for the user to delete a given user to improve security.
@router.delete("/delete-user/")
async def delete_user(user: User, request: Request):
    await is_user_admin(request)
    try:
        await controls.delete_user(user)
        return JSONResponse(content={"message": "successfully deleted user"}, status_code=200)
    except:
        return JSONResponse(content={"message": "not successful deleting user"}, status_code=403)

@router.get("/fetch-all-users/")
async def fetch_all_users(request: Request):
    await get_cookie(request)
    try:
        all_users = await controls.fetch_all_users()
        all_users = [user.dict() for user in all_users]
        return JSONResponse(content={"message": "successfully fetched all users", 'all_users': all_users}, status_code=200)
    except:
        return JSONResponse(content={"message": "not successful deleting user"}, status_code=403)

@router.post("/create-shift/")
async def create_shift(shift: Shift, request: Request):
    await is_user_admin(request)
    try:
        await controls.create_shift(shift)
        return JSONResponse(content={"message": "successfully created shift"}, status_code=200)
    except:
        return JSONResponse(content={"message": "not successful creating shift"}, status_code=403)

@router.get("/fetch-shift/")
async def fetch_shift(shift: Shift, request: Request):
    get_cookie(request)
    try:
        _shift = await controls.get_shift(shift)
        return JSONResponse(content={"message": "Successfully fetched shift", "shift": _shift.dict()}, status_code=200)
    except:
        return JSONResponse(content={"message": "not successful fetching shift"}, status_code=403)

class ShiftRequest(BaseModel):
    chosen_date: date  # Ensure the type and field name are correct

@router.post("/fetch-shifts-for-month/")
async def fetch_shifts_for_month(chosen_date: ShiftRequest, request: Request):
    chosen_date = chosen_date.chosen_date
    uid_user = get_cookie(request)
    user = User(uid_user=uid_user)
    try:
        print("hi")
        month_calender = await controls.get_shifts_for_month(chosen_date, user)
        print("hi")
        return JSONResponse(content={"message": "successfully fetched all shifts for month", "shifts": month_calender.dict()}, status_code=200)
    except:
        return JSONResponse(content={"message": "not successful fetching all shifts for month"}, status_code=403)

@router.delete("/delete-shift/")
async def delete_shift(shift: Shift, request: Request):
    await is_user_admin(request)
    try:
        await controls.delete_shift(shift)
        return JSONResponse(content={"message": "successfully deleted shift"}, status_code=200)
    except:
        return JSONResponse(content={"message": "not successful deleting shift"}, status_code=403)

@router.options("/hi/")
async def test_options():
    return