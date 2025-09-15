from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from app.role.repositories.role_repo import RoleRepo


async def get_role_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> RoleRepo:
    return RoleRepo(db)


