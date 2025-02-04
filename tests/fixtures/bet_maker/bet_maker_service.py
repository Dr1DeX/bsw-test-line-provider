import json
from dataclasses import dataclass
from unittest.mock import AsyncMock

import pytest

from tests.fixtures.bet_maker.bet_maker_schema import (
    TestBetBaseSchema,
    TestBetCreateSchema,
    TestBetsSchema,
    TestEventSchema,
)


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

    async def get_events(self) -> list[TestEventSchema]:
        events = await self.bet_read_repository.get_events()
        return [TestEventSchema.model_validate(event) for event in events]

    async def get_bets(self) -> list[TestBetsSchema]:
        bets = await self.bet_read_repository.get_bets()
        return [TestBetsSchema(event_id=bet.event_id, status=bet.status) for bet in bets]

    async def create_bet(self, bet: TestBetCreateSchema) -> TestBetBaseSchema:
        event_id = await self.bet_write_repository.create_bet(bet=bet)
        return TestBetBaseSchema(event_id=event_id)


@pytest.fixture
def bet_service(bet_write_repository, bet_read_repository):
    return FakeBetService(bet_write_repository=bet_write_repository, bet_read_repository=bet_read_repository)
