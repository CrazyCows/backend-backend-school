from datetime import datetime

from pydantic import BaseModel
from typing import List, Optional

from models.users_model import User


class ShiftMember(User):
    uid_shift: str
    attendance: bool #Attended the shift or skipped work/got sick
    wished: bool #wished for the shift or not, to be prioritised
    activemember: bool #true if the member has been assigned the shift

class Shift(BaseModel):
    uid_shift: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    wished_shift_members: Optional[List[ShiftMember]] = None
    actual_shift_members: Optional[List[ShiftMember]] = None
    active: Optional[bool] = None
    description: Optional[str] = None

class Calender(BaseModel):
    shifts: List[Shift]
    month: str
    year: str

class Clearnce_lvl(BaseModel):
    id_actual: str
    role: str