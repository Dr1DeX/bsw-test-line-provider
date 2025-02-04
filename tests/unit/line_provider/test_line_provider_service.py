import time

import pytest

from tests.fixtures.line_provider.line_provider_schema import (
    TestEventCreateSchema,
    TestEventStatus,
    TestEventUpdateSchema,
)


pytestmark = pytest.mark.asyncio


async def test_line_provider_create_event(line_provider_service):
    event = TestEventCreateSchema(coefficient=100.1, deadline=int(time.time()) + 600, status=TestEventStatus.NEW)

    result = await line_provider_service.create_event(event=event)
    assert result["event_id"] == "123"


async def test_line_provider_update_event_status(line_provider_service):
    new_status = TestEventUpdateSchema(event_id="132", status=TestEventStatus.FINISHED_WIN)

    result = await line_provider_service.update_event_status(new_status=new_status)
    result == 1
