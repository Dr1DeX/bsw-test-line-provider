import asyncio
import json
import logging
from dataclasses import dataclass
from typing import Sequence

from sqlalchemy import (
    insert,
    select,
    update,
)
from sqlalchemy.ext.asyncio import AsyncSession

import aio_pika.abc

from src.bet_maker.models import Bets
from src.bet_maker.schema import BetsCreateSchema
from src.infrastructure.broker.accessor import get_broker_connection
from src.producer import send_to_queue


@dataclass
class BetsWriteRepository:
    db_session: AsyncSession

    async def create_bet(self, bet: BetsCreateSchema) -> int | None:
        payload = {"event_id": bet.event_id, "action": "get_event"}
        await send_to_queue(exchange_name="line_provider_exchange", routing_key="bet_events", payload=payload)
        connection = await get_broker_connection()
        status = None
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(name="events", durable=True)

            async def on_message(msg: aio_pika.abc.AbstractIncomingMessage):
                nonlocal status
                async with msg.process():
                    try:
                        data = json.loads(msg.body.decode())
                        logging.info(f"[bet-maker] Received data: {data}")
                        events_from_msg = data.get("status", "")
                        if events_from_msg:
                            status = events_from_msg
                    except Exception as e:
                        logging.error(f"[bet-maker] Error msg: {e}")

            await queue.consume(on_message)
            await asyncio.sleep(2)

        if status is not None:
            query = (
                insert(Bets).values(event_id=bet.event_id, sum_bet=bet.sum_bet, status=status).returning(Bets.event_id)
            )

            async with self.db_session as session:
                event_id = (await session.execute(query)).scalar_one_or_none()
                await session.commit()
                return event_id
        logging.warning("[bet-maker] Status not received")

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
    async def get_events() -> list:
        payload = {"action": "get_events"}
        await send_to_queue(exchange_name="line_provider_exchange", routing_key="bet_events", payload=payload)
        events = []

        connection = await get_broker_connection()
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(name="events", durable=True)

            async def on_message(msg: aio_pika.abc.AbstractIncomingMessage):
                async with msg.process():
                    try:
                        data = json.loads(msg.body.decode())
                        logging.info(f"[bet-maker] Received data: {data}")
                        events_from_msg = data.get("events", [])
                        if events_from_msg:
                            events.extend(events_from_msg)
                    except Exception as e:
                        logging.error(f"[bet-maker] Error msg: {e}")

            await queue.consume(on_message)
            await asyncio.sleep(2)

            return events
