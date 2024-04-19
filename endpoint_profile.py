from fastapi import APIRouter, Depends, Request, Response, HTTPException
from fastapi.responses import JSONResponse
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
    encrypted_data = request.cookies.get("secure_cookie")
    if encrypted_data:
        decrypted_data = decrypt_data(encrypted_data)
        return decrypted_data # Should be userId (for the love of god)
    raise HTTPException(status_code=403)


# TODO: Discuss if this should return
@router.post("/create-user/")
async def create_user(user: CreateUser, request: Request):
    get_cookie(request)
    try:
        await controls.create_user(user)
        return JSONResponse(content={"message": "successfully created user"}, status_code=201)
    except:
        return JSONResponse(content={"message": "not successful creating user"}, status_code=403)


@router.post("/user-login/")
async def user_login(user: UserLogin, response: Response):
    try:

        print("hi")
        print(user)
        current_user = await controls.login(user)
        data = current_user.uid_user
        encrypted_data = encrypt_data(data)
        response.set_cookie(key="secure_cookie", value=encrypted_data, max_age=max_age)
        return JSONResponse(content={"message": "successfully logged in user"}, status_code=200)
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
        return JSONResponse(content={"message": "successfully created shift"}, status_code=200)
    except:
        return JSONResponse(content={"message": "not successful creating shift"}, status_code=403)

@router.get("/fetch-shift/")
async def fetch_shift(shift: Shift = Depends(Shift)):
    try:
        _shift = await controls.get_shift(shift)
        return JSONResponse(content={"message": "Successfully fetched shift", "shift": _shift.dict()}, status_code=200)
    except:
        return JSONResponse(content={"message": "not successful fetching shift"}, status_code=403)

@router.get("/fetch-shifts-for-month/")
async def fetch_shifts_for_month(date: Depends(date), user: Depends(User)):
    try:
        month_shifts = await controls.get_shifts_for_month(date, user)
        return JSONResponse(content={"message": "successfully fetched all shifts for month", "shifts": month_shifts.dict()}, status_code=200)
    except:
        return JSONResponse(content={"message": "not successful fetching all shifts for month"}, status_code=403)

@router.delete("/delete-shift/")
async def delete_shift(shift: Depends(Shift)):
    try:
        await controls.delete_shift(shift)
        return JSONResponse(content={"message": "successfully deleted shift"}, status_code=200)
    except:
        return JSONResponse(content={"message": "not successful deleting shift"}, status_code=403)

@router.options("/hi/")
async def test_options():
    return