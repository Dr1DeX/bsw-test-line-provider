from dataclasses import dataclass
from unittest.mock import AsyncMock

import pytest

from tests.fixtures.line_provider.line_provider_schema import TestEventCreateSchema


@dataclass
class FakeLineProviderService:
    line_provider_read_repository: AsyncMock
    line_provider_write_repository: AsyncMock

    async def create_event(self, event: TestEventCreateSchema) -> dict:
        await self.line_provider_read_repository.create_event(event=event)
        return {"event_id": "123"}

    async def update_event_status(self, new_status) -> int:
        await self.line_provider_write_repository.update_event_status(new_status=new_status)
        return 1


@pytest.fixture
def line_provider_service(line_provider_read_repository, line_provider_write_repository):
    return FakeLineProviderService(
        line_provider_read_repository=line_provider_read_repository,
        line_provider_write_repository=line_provider_write_repository,
    )
