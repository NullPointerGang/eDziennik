from pydantic import BaseModel, EmailStr
from typing import List


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    roles: List[str] = []


