from datetime import datetime

from pydantic import BaseModel
from typing import List, Optional

from src.models.users_model import User


class ShiftMember(User):
    attendance: Optional[str] = None #Attended the shift or skipped work/got sick
    wished: Optional[bool] = None #wished for the shift or not, to be prioritised
    active_member: Optional[bool] = None #true if the member has been assigned the shift

class Shift(BaseModel):
    uid_shift: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    wished_shift_members: Optional[List[ShiftMember]] = None
    actual_shift_members: Optional[List[ShiftMember]] = None
    active: Optional[bool] = None
    myShift: Optional[bool] = None

class Calender(BaseModel):
    shifts: List[Shift]
    month: str
    year: str

class Clearnce_lvl(BaseModel):
    id_actual: str
    role: str