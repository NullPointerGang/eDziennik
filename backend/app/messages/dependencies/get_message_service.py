from typing import Annotated
from fastapi import Depends
from app.messages.repositories.message_repo import MessageRepo
from app.messages.services.message_service import MessageService
from app.messages.dependencies.get_message_repo import get_message_repo


async def get_message_service(repo: Annotated[MessageRepo, Depends(get_message_repo)]) -> MessageService:
    return MessageService(repo)


