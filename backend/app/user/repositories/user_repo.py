from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.user.schemas.user_schem import User


class UserRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_users(self) -> List[User]:
        result = await self.db.execute(select(User).options(selectinload(User.roles)))
        return list(result.scalars().all())

    async def get_user(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User).options(selectinload(User.roles)).where(User.id == user_id)
        )
        return result.scalars().first()


