from typing import Annotated
from fastapi import Depends
from app.schedule.repositories.schedule_repo import ScheduleRepo
from app.schedule.services.schedule_service import ScheduleService
from app.schedule.dependencies.get_schedule_repo import get_schedule_repo


async def get_schedule_service(repo: Annotated[ScheduleRepo, Depends(get_schedule_repo)]) -> ScheduleService:
    return ScheduleService(repo)


