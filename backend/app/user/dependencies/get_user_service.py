from typing import Annotated
from fastapi import Depends
from app.user.repositories.user_repo import UserRepo
from app.user.services.user_service import UserService
from app.user.dependencies.get_user_repo import get_user_repo


async def get_user_service(repo: Annotated[UserRepo, Depends(get_user_repo)]) -> UserService:
    return UserService(repo)


