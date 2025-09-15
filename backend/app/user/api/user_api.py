from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from app.user.dependencies.get_user_service import get_user_service
from app.user.services.user_service import UserService
from app.user.models.user_model import UserResponse


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def list_users(service: Annotated[UserService, Depends(get_user_service)]):
    users = await service.list_users()
    data: List[UserResponse] = []
    for u in users:
        data.append(UserResponse(
            id=u.id,
            email=u.email,
            first_name=u.first_name,
            last_name=u.last_name,
            roles=[r.name for r in (u.roles or [])]
        ))
    return data


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, service: Annotated[UserService, Depends(get_user_service)]):
    u = await service.get_user(user_id)
    if not u:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse(
        id=u.id,
        email=u.email,
        first_name=u.first_name,
        last_name=u.last_name,
        roles=[r.name for r in (u.roles or [])]
    )


