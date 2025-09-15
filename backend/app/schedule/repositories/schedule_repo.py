from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.schedule.schemas.schedule_schem import ScheduleItem


class ScheduleRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_items(self, class_name: Optional[str] = None, weekday: Optional[int] = None) -> List[ScheduleItem]:
        stmt = select(ScheduleItem)
        if class_name is not None:
            stmt = stmt.where(ScheduleItem.class_name == class_name)
        if weekday is not None:
            stmt = stmt.where(ScheduleItem.weekday == weekday)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_item(self, item_id: int) -> Optional[ScheduleItem]:
        result = await self.db.execute(select(ScheduleItem).where(ScheduleItem.id == item_id))
        return result.scalars().first()

    async def create_item(self, payload: dict) -> ScheduleItem:
        item = ScheduleItem(**payload)
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update_item(self, item_id: int, payload: dict) -> Optional[ScheduleItem]:
        await self.db.execute(
            update(ScheduleItem)
            .where(ScheduleItem.id == item_id)
            .values(**payload)
        )
        await self.db.commit()
        return await self.get_item(item_id)

    async def delete_item(self, item_id: int) -> None:
        await self.db.execute(delete(ScheduleItem).where(ScheduleItem.id == item_id))
        await self.db.commit()


