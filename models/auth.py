from pydantic import BaseModel

class Token(BaseModel):
    token: str

class UserInfo(BaseModel):
    user_id: str
    email: str
