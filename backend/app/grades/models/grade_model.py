from datetime import date
from pydantic import BaseModel
from typing import Optional, List


class GradeCreate(BaseModel):
    student_id: int
    teacher_id: int
    subject: str
    value: int
    date: date
    comment: Optional[str] = None


class GradeUpdate(BaseModel):
    subject: Optional[str] = None
    value: Optional[int] = None
    date: Optional[date] = None
    comment: Optional[str] = None


class GradeResponse(BaseModel):
    id: int
    student_id: int
    teacher_id: int
    subject: str
    value: int
    date: date
    comment: Optional[str] = None


