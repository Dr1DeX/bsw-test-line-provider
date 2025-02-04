import json
import time
from unittest.mock import AsyncMock

import pytest

from tests.fixtures.bet_maker.bet_maker_schema import (
    TestBetCreateSchema,
    TestBetsSchema,
    TestEventSchema,
    TestEventStatus,
)


pytestmark = pytest.mark.asyncio


async def test_handle_update_event(bet_service):
    message = AsyncMock()
    message.body = json.dumps({"event_id": "event_1", "status": "NEW", "action": "update_event"})

    res = await bet_service.handle_update_event(message)
    assert res == 1


async def test_get_events(bet_service):
    result = await bet_service.get_events()

    assert result == [
        TestEventSchema(
            event_id="event_1",
            coefficient=1.01,
            deadline=int(time.time()) + 600,
            status=TestEventStatus.NEW,
        ),
    ]


async def test_get_bets(bet_service):
    result = await bet_service.get_bets()

    assert result == [TestBetsSchema(event_id="event_1", status=TestEventStatus.NEW)]


async def test_create_bet(bet_service):
    bet = TestBetCreateSchema(event_id="event_id_123", sum_bet=100.12)

    result = await bet_service.create_bet(bet=bet)
    assert result.event_id == "event_id_123"
