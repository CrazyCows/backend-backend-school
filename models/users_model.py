from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    user_uid: Optional[str] = None
    name: str
    email: str
    phone: Optional[str] = None
    role: str

class UserLogin(BaseModel):
    username: str
    password: str

class CreateUser(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    role: str
    username: str
    password: str