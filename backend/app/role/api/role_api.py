from fastapi import APIRouter, Depends, status
from typing import Annotated, List
from app.role.dependencies.get_role_service import get_role_service
from app.role.services.role_service import RoleService
from app.role.models.role_model import RoleCreate, RoleResponse


router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/", response_model=List[RoleResponse], status_code=status.HTTP_200_OK)
async def list_roles(service: Annotated[RoleService, Depends(get_role_service)]):
    roles = await service.list_roles()
    return [RoleResponse(id=r.id, name=r.name) for r in roles]


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(payload: RoleCreate, service: Annotated[RoleService, Depends(get_role_service)]):
    role = await service.create_role(payload.name)
    return RoleResponse(id=role.id, name=role.name)


