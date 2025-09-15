from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from app.user.repositories.user_repo import UserRepo


async def get_user_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> UserRepo:
    return UserRepo(db)


