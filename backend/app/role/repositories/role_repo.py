from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.user.schemas.role_schem import Roles


class RoleRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_roles(self) -> List[Roles]:
        result = await self.db.execute(select(Roles))
        return list(result.scalars().all())

    async def create_role(self, name: str) -> Roles:
        role = Roles(name=name)
        self.db.add(role)
        await self.db.commit()
        await self.db.refresh(role)
        return role


