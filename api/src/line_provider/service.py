from dataclasses import dataclass

from src.line_provider.repository import (
    LineProviderReadRepository,
    LineProviderWriteRepository,
)
from src.line_provider.schema import (
    EventCreateSchema,
    EventUpdateSchema,
)


@dataclass
class LineProviderService:
    line_provider_write_repo: LineProviderWriteRepository
    line_provider_read_repo: LineProviderReadRepository

    async def create_event(self, event: EventCreateSchema) -> dict:
        return await self.line_provider_write_repo.create_event(event=event)

    async def update_event_status(self, new_status: EventUpdateSchema) -> None:
        await self.line_provider_write_repo.update_event_status(new_status=new_status)
