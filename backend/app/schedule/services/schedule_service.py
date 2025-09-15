from typing import List, Optional
from app.schedule.repositories.schedule_repo import ScheduleRepo
from app.schedule.schemas.schedule_schem import ScheduleItem


class ScheduleService:
    def __init__(self, repo: ScheduleRepo):
        self.repo = repo

    async def list_items(self, class_name: Optional[str] = None, weekday: Optional[int] = None) -> List[ScheduleItem]:
        return await self.repo.list_items(class_name, weekday)

    async def get_item(self, item_id: int) -> Optional[ScheduleItem]:
        return await self.repo.get_item(item_id)

    async def create_item(self, payload: dict) -> ScheduleItem:
        return await self.repo.create_item(payload)

    async def update_item(self, item_id: int, payload: dict) -> Optional[ScheduleItem]:
        return await self.repo.update_item(item_id, payload)

    async def delete_item(self, item_id: int) -> None:
        await self.repo.delete_item(item_id)


