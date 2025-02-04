import json
from unittest.mock import AsyncMock

import pytest


pytestmark = pytest.mark.asyncio


async def test_handle_update_event(bet_service, bet_write_repository):
    message = AsyncMock()
    message.body = json.dumps({"event_id": "event_1", "status": "NEW", "action": "update_event"})

    res = await bet_service.handle_update_event(message)
    assert res == 1
