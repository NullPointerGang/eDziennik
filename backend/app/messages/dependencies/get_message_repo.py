from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from app.messages.repositories.message_repo import MessageRepo


async def get_message_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> MessageRepo:
    return MessageRepo(db)


