import time
from unittest.mock import AsyncMock

import pytest

from tests.fixtures.bet_maker.bet_maker_schema import (
    TestBetsSchema,
    TestEventSchema,
    TestEventStatus,
)


@pytest.fixture
def bet_write_repository():
    repository = AsyncMock()
    repository.update_status_bet = AsyncMock()
    repository.create_bet = AsyncMock(return_value="event_id_123")
    return repository


@pytest.fixture
def bet_read_repository():
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
    repository.get_bets = AsyncMock(return_value=[TestBetsSchema(event_id="event_1", status=TestEventStatus.NEW)])
    return repository
