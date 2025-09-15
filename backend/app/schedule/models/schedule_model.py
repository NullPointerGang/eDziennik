from pydantic import BaseModel
from typing import Optional, List


class ScheduleCreate(BaseModel):
    class_name: str
    weekday: int
    time_from: str
    time_to: str
    subject: str
    teacher_id: Optional[int] = None


class ScheduleUpdate(BaseModel):
    class_name: Optional[str] = None
    weekday: Optional[int] = None
    time_from: Optional[str] = None
    time_to: Optional[str] = None
    subject: Optional[str] = None
    teacher_id: Optional[int] = None


class ScheduleResponse(BaseModel):
    id: int
    class_name: str
    weekday: int
    time_from: str
    time_to: str
    subject: str
    teacher_id: Optional[int] = None


