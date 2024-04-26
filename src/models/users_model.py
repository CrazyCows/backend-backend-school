from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    uid_user: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None

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

