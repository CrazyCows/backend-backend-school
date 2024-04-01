from pydantic import BaseModel
from typing import List

class ShiftMember(BaseModel):
    shift_id: str
    user_uid: str
    attendance: bool

class Shift(BaseModel):
    uid_shift: str
    start_time: str
    end_time: str
    wished_shift_members: List[ShiftMember]
    actual_shift_members: List[ShiftMember]
    active: bool
    description: str

class Calender(BaseModel):
    shifts: List[Shift]
    month: str
    year: str

class Clearnce_lvl(BaseModel):
    id_actual: str
    role: str