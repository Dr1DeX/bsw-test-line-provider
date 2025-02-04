import time
from unittest.mock import AsyncMock

import pytest

from tests.fixtures.line_provider.line_provider_schema import (
    TestEventSchema,
    TestEventStatus,
)


@pytest.fixture
def line_provider_write_repository():
    repository = AsyncMock()
    repository.create_event = AsyncMock(return_value={"event_id": "123"})
    repository.update_event_status = AsyncMock(return_value=1)
    return repository


@pytest.fixture
def line_provider_read_repository():
    repository = AsyncMock()
    repository.get_events = AsyncMock(
        return_value=[
            TestEventSchema(
                event_id="event_1",
                coefficient=1.01,
                deadline=int(time.time()) + 600,
                state=TestEventStatus.NEW,
            ),
        ],
    )
    repository.get_event = AsyncMock(
        TestEventSchema(
            event_id="123",
            coefficient=100.11,
            status=TestEventStatus.NEW,
            deadline=int(time.time()) + 600,
        ),
    )
    return repository
