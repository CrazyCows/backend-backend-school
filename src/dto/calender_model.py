from datetime import datetime, date

from pydantic import BaseModel
from typing import List, Optional

from src.dto.users_model import User


class ShiftMember(User):
    uid_shift: Optional[str] = None
    attendance: Optional[bool] = None  # Attended the shift or skipped work/got sick
    wished: Optional[bool] = None  # wished for the shift or not, to be prioritised
    assigned: Optional[bool] = None  # true if the member has been assigned the shift


class Shift(BaseModel):
    uid_shift: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    wished_shift_members: Optional[List[ShiftMember]] = None
    actual_shift_members: Optional[List[ShiftMember]] = None
    active: Optional[bool] = None
    myShift: Optional[bool] = None


class Calender(BaseModel):
    shifts: list
    month: int
    year: int

    def to_dict(self):
        return {
            "shifts": [{
                "uid_shift": shift.uid_shift,
                "start_time": shift.start_time.isoformat() if shift.start_time else None,
                "end_time": shift.end_time.isoformat() if shift.end_time else None,
                "wished_shift_members": [],
                "actual_shift_members": [],
                "active": shift.active,
                "myShift": shift.myShift if shift.myShift is not None else False
            } for shift in self.shifts],
            "month": self.month,
            "year": self.year
        }


class Clearnce_lvl(BaseModel):
    id_actual: str
    role: str

class ShiftRequest(BaseModel):
    chosen_date: date  # Ensure the type and field name are correct
