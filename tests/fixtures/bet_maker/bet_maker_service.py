import json
from dataclasses import dataclass
from unittest.mock import AsyncMock

import pytest


@dataclass
class FakeBetService:
    bet_write_repository: AsyncMock
    bet_read_repository: AsyncMock

    async def handle_update_event(self, message: AsyncMock):
        data = json.loads(message.body)
        event_id = data.get("event_id")
        status = data.get("status")
        action = data.get("action")

        if not event_id or not status:
            return

        if action == "update_event":
            await self.bet_write_repository.update_status_bet(event_id=event_id, status=status)
            return 1


@pytest.fixture
def bet_service(bet_write_repository, bet_read_repository):
    return FakeBetService(bet_write_repository=bet_write_repository, bet_read_repository=bet_read_repository)
