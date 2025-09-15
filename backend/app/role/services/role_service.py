from typing import List
from app.user.schemas.role_schem import Roles
from app.role.repositories.role_repo import RoleRepo


class RoleService:
    def __init__(self, role_repo: RoleRepo):
        self.role_repo = role_repo

    async def list_roles(self) -> List[Roles]:
        return await self.role_repo.list_roles()

    async def create_role(self, name: str) -> Roles:
        return await self.role_repo.create_role(name)


