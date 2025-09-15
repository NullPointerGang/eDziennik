from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class MessageCreate(BaseModel):
    from_id: int
    to_id: Optional[int] = None
    class_name: Optional[str] = None
    content: str


class MessageResponse(BaseModel):
    id: int
    from_id: int
    to_id: Optional[int] = None
    class_name: Optional[str] = None
    content: str
    created_at: datetime


