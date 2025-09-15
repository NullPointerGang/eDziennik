from typing import List, Optional
from app.messages.repositories.message_repo import MessageRepo
from app.messages.schemas.message_schem import Message


class MessageService:
    def __init__(self, repo: MessageRepo):
        self.repo = repo

    async def send(self, payload: dict) -> Message:
        return await self.repo.send(payload)

    async def list_messages(
        self,
        from_id: Optional[int] = None,
        to_id: Optional[int] = None,
        class_name: Optional[str] = None,
    ) -> List[Message]:
        return await self.repo.list_messages(from_id, to_id, class_name)


