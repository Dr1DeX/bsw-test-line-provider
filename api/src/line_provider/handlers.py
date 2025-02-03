from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from src.dependency import get_line_provider_service
from src.line_provider.schema import (
    EventCreateSchema,
    EventUpdateSchema,
)
from src.line_provider.service import LineProviderService


router = APIRouter(prefix="/api/v1/provider", tags=["provider"])


@router.post(
    "/event",
)
async def create_event(
    line_provider_service: Annotated[LineProviderService, Depends(get_line_provider_service)],
    event: EventCreateSchema,
):
    return await line_provider_service.create_event(event=event)


@router.put("/event/status")
async def update_event_status(
    line_provider_service: Annotated[LineProviderService, Depends(get_line_provider_service)],
    new_status: EventUpdateSchema,
):
    await line_provider_service.update_event_status(new_status=new_status)
