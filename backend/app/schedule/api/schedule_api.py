from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.schedule.dependencies.get_schedule_service import get_schedule_service
from app.schedule.services.schedule_service import ScheduleService
from app.schedule.models.schedule_model import (
    ScheduleCreate,
    ScheduleUpdate,
    ScheduleResponse,
)


router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.get("/", response_model=List[ScheduleResponse], status_code=status.HTTP_200_OK)
async def list_items(
    service: Annotated[ScheduleService, Depends(get_schedule_service)],
    class_name: Optional[str] = Query(default=None),
    weekday: Optional[int] = Query(default=None),
):
    items = await service.list_items(class_name, weekday)
    return [ScheduleResponse(**i.__dict__) for i in items]


@router.get("/{item_id}", response_model=ScheduleResponse, status_code=status.HTTP_200_OK)
async def get_item(item_id: int, service: Annotated[ScheduleService, Depends(get_schedule_service)]):
    i = await service.get_item(item_id)
    if not i:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule item not found")
    return ScheduleResponse(**i.__dict__)


@router.post("/", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_item(payload: ScheduleCreate, service: Annotated[ScheduleService, Depends(get_schedule_service)]):
    i = await service.create_item(payload.dict())
    return ScheduleResponse(**i.__dict__)


@router.patch("/{item_id}", response_model=ScheduleResponse, status_code=status.HTTP_200_OK)
async def update_item(item_id: int, payload: ScheduleUpdate, service: Annotated[ScheduleService, Depends(get_schedule_service)]):
    i = await service.update_item(item_id, {k: v for k, v in payload.dict().items() if v is not None})
    if not i:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule item not found")
    return ScheduleResponse(**i.__dict__)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, service: Annotated[ScheduleService, Depends(get_schedule_service)]):
    await service.delete_item(item_id)
    return None


