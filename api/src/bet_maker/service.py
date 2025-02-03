import json
import logging
from dataclasses import dataclass

import aio_pika.abc

from src.bet_maker.repository import (
    BetsReadRepository,
    BetsWriteRepository,
)
from src.bet_maker.schema import (
    BetsBaseSchema,
    BetsCreateSchema,
    BetsSchema,
)
from src.line_provider.schema import EventSchema


@dataclass
class BetService:
    bet_write_repository: BetsWriteRepository
    bet_read_repository: BetsReadRepository

    async def handle_update_event(self, message: aio_pika.abc.AbstractIncomingMessage) -> None:
        async with message.process():
            data = json.loads(message.body.decode())
            event_id = data.get("event_id")
            status = data.get("status")

            if not event_id or not status:
                logging.error("Uncorrected data for update")
                return
            await self.bet_write_repository.update_status_bet(event_id=event_id, status=status)

    async def create_bet(self, bet: BetsCreateSchema) -> BetsBaseSchema:
        event_id = await self.bet_write_repository.create_bet(bet=bet)
        return BetsBaseSchema(event_id=event_id)

    async def get_events(self) -> list[EventSchema]:
        events = await self.bet_read_repository.get_events()
        events_schema = [EventSchema.model_validate(event) for event in events]
        return events_schema

    async def get_bets(self) -> list[BetsSchema]:
        bets = await self.bet_read_repository.get_bets()
        bets_schema = [BetsSchema.model_validate(bet) for bet in bets]
        return bets_schema
