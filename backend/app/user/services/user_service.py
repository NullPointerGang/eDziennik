from typing import List, Optional
from app.user.repositories.user_repo import UserRepo
from app.user.schemas.user_schem import User


class UserService:
    def __init__(self, repo: UserRepo):
        self.repo = repo

    async def list_users(self) -> List[User]:
        return await self.repo.list_users()

    async def get_user(self, user_id: int) -> Optional[User]:
        return await self.repo.get_user(user_id)


