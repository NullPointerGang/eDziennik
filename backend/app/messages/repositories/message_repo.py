from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.messages.schemas.message_schem import Message


class MessageRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def send(self, payload: dict) -> Message:
        msg = Message(**payload)
        self.db.add(msg)
        await self.db.commit()
        await self.db.refresh(msg)
        return msg

    async def list_messages(
        self,
        from_id: Optional[int] = None,
        to_id: Optional[int] = None,
        class_name: Optional[str] = None,
    ) -> List[Message]:
        stmt = select(Message)
        if from_id is not None:
            stmt = stmt.where(Message.from_id == from_id)
        if to_id is not None:
            stmt = stmt.where(Message.to_id == to_id)
        if class_name is not None:
            stmt = stmt.where(Message.class_name == class_name)
        result = await self.db.execute(stmt.order_by(Message.created_at))
        return list(result.scalars().all())


