import json
import logging

import aio_pika

from src.infrastructure.broker.accessor import get_broker_connection


async def send_to_queue(
    exchange_name: str,
    routing_key: str,
    payload: dict,
) -> None:
    try:
        connection = await get_broker_connection()
        logging.info("[!] Sendler connection established")
        channel = await connection.channel()

        exchange = await channel.declare_exchange(
            name=exchange_name,
            type=aio_pika.ExchangeType.DIRECT,
        )
        message = aio_pika.Message(
            body=json.dumps(payload).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        await exchange.publish(
            message=message,
            routing_key=routing_key,
        )
        logging.info(
            f"Stargazer sent to {exchange_name} with routing_key {routing_key}",
        )
    except Exception as e:
        logging.error(f"[!] Failed stargazer-spot: {e}")
        raise
