from pydantic import BaseModel

class User(BaseModel):
    user_uid: str
    user_name: str
    email: str
    role: str

class UserLogin(BaseModel):
    username: str
    password: str