import asyncio
import logging

import aio_pika

from src.dependency import (
    get_bet_read_repository,
    get_bet_service,
    get_bet_write_repository,
)
from src.infrastructure.broker.accessor import get_broker_connection
from src.infrastructure.database.accessor import AsyncSessionFactory


async def make_line_provider_consumer():
    bet_read_repo = await get_bet_read_repository(db_session=AsyncSessionFactory())
    bet_write_repo = await get_bet_write_repository(db_session=AsyncSessionFactory())
    bet_service = await get_bet_service(bet_read_repository=bet_read_repo, bet_write_repository=bet_write_repo)
    while True:
        try:
            connection = await get_broker_connection()
            async with connection:
                channel = await connection.channel()
                exchange = await channel.declare_exchange(
                    name="line_provider_exchange",
                    type=aio_pika.ExchangeType.DIRECT,
                )
                queue = await channel.declare_queue(name="update_event", durable=True)
                await queue.bind(exchange=exchange, routing_key="update_event")
                await queue.consume(bet_service.handle_update_event)

                await asyncio.Future()
        except (
            aio_pika.exceptions.AMQPConnectionError,
            aio_pika.exceptions.ChannelInvalidStateError,
        ) as e:
            logging.warning(f"[!] Connection error: {e}. Retrying in 10 seconds...")
            await asyncio.sleep(10)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise
