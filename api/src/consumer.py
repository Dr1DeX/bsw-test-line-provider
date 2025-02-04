import aio_pika

from src.dependency import (
    get_bet_read_repository,
    get_bet_service,
    get_bet_write_repository,
    get_line_provider_read_repository,
    get_line_provider_service,
    get_line_provider_write_repository,
)
from src.infrastructure.broker.accessor import get_broker_connection
from src.infrastructure.database.accessor import AsyncSessionFactory
from src.infrastructure.storage.accessor import get_redis_connection


async def make_provider_consumer():
    bet_read_repo = await get_bet_read_repository(db_session=AsyncSessionFactory())
    bet_write_repo = await get_bet_write_repository(db_session=AsyncSessionFactory())
    bet_service = await get_bet_service(bet_read_repository=bet_read_repo, bet_write_repository=bet_write_repo)
    redis_client = await get_redis_connection()
    line_provider_read_repo = await get_line_provider_read_repository(redis_client=redis_client)
    line_provider_write_repo = await get_line_provider_write_repository(redis_client=redis_client)
    line_provider_service = await get_line_provider_service(
        line_provider_read_repo=line_provider_read_repo,
        line_provider_write_repo=line_provider_write_repo,
    )
    connection = await get_broker_connection()
    channel = await connection.channel()
    bet_exchange = await channel.declare_exchange(
        name="bet_maker_exchange",
        type=aio_pika.ExchangeType.DIRECT,
    )
    bet_queue = await channel.declare_queue(name="update_event", durable=True)
    events_queue = await channel.declare_queue(name="events", durable=True)
    await events_queue.bind(exchange=bet_exchange)

    await bet_queue.bind(exchange=bet_exchange)
    await bet_queue.consume(bet_service.handle_update_event)

    line_exchange = await channel.declare_exchange(name="line_provider_exchange", type=aio_pika.ExchangeType.DIRECT)
    line_queue = await channel.declare_queue(name="bet_events", durable=True)
    await line_queue.bind(exchange=line_exchange)
    await line_queue.consume(callback=line_provider_service.handle_rpc_request)
