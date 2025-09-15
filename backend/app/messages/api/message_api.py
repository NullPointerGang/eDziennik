from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, Query, status
from app.messages.dependencies.get_message_service import get_message_service
from app.messages.services.message_service import MessageService
from app.messages.models.message_model import MessageCreate, MessageResponse
from app.auth.dependencies.get_current_user_id import get_current_user_id


router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    payload: MessageCreate,
    service: Annotated[MessageService, Depends(get_message_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
):
    data = payload.dict()
    if data.get("from_id") is None:
        data["from_id"] = current_user_id
    m = await service.send(data)
    return MessageResponse(**m.__dict__)


@router.get("/", response_model=List[MessageResponse], status_code=status.HTTP_200_OK)
async def list_messages(
    service: Annotated[MessageService, Depends(get_message_service)],
    current_user_id: Annotated[int, Depends(get_current_user_id)],
    from_id: Optional[int] = Query(default=None),
    to_id: Optional[int] = Query(default=None),
    class_name: Optional[str] = Query(default=None),
):
    if from_id is None and to_id is None and class_name is None:
        from_id = current_user_id
    messages = await service.list_messages(from_id, to_id, class_name)
    return [MessageResponse(**m.__dict__) for m in messages]


