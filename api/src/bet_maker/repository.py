from dataclasses import dataclass
from typing import Sequence

from sqlalchemy import (
    insert,
    select,
    update,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.bet_maker.models import Bets
from src.bet_maker.schema import BetsCreateSchema
from src.producer import rpc_call


@dataclass
class BetsWriteRepository:
    db_session: AsyncSession

    async def create_bet(self, bet: BetsCreateSchema) -> int:
        payload = {"event_id": bet.event_id, "action": "get_event"}
        response = await rpc_call(exchange_name="line_provider_exchange", routing_key="get_event", payload=payload)
        status = response.get("status")
        if not status:
            raise ValueError("Failed to get the status of an event")
        query = insert(Bets).values(event_id=bet.event_id, sum_bet=bet.sum_bet, status=status).returning(Bets.event_id)

        async with self.db_session as session:
            event_id = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            return event_id

    async def update_status_bet(self, status: str, event_id: int) -> None:
        query = update(Bets).values(status=status).where(Bets.event_id == event_id)
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()


@dataclass
class BetsReadRepository:
    db_session: AsyncSession

    async def get_bets(self) -> Sequence[Bets]:
        query = select(Bets)

        async with self.db_session as session:
            bets = (await session.execute(query)).scalars().all()
            return bets

    @staticmethod
    async def get_events():
        payload = {"action": "get_events"}
        response = await rpc_call(exchange_name="line_provider_exchange", routing_key="get_events", payload=payload)
        events = response.get("events", [])
        return events
