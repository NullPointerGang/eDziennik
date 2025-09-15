from typing import Annotated
from fastapi import Depends
from app.role.dependencies.get_role_repo import get_role_repo
from app.role.repositories.role_repo import RoleRepo
from app.role.services.role_service import RoleService


async def get_role_service(repo: Annotated[RoleRepo, Depends(get_role_repo)]) -> RoleService:
    return RoleService(repo)


