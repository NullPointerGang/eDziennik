from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from app.schedule.repositories.schedule_repo import ScheduleRepo


async def get_schedule_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> ScheduleRepo:
    return ScheduleRepo(db)


