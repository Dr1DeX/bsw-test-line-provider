import asyncio
import json

import aio_pika

from src.infrastructure.broker.accessor import get_broker_connection


async def rpc_call(exchange_name: str, routing_key: str, payload: dict) -> dict:
    connection = await get_broker_connection()
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(exchange_name, aio_pika.ExchangeType.DIRECT)
        callback_queue = await channel.declare_queue(exclusive=True)

        message = aio_pika.Message(
            json.dumps(payload).encode(),
            reply_to=callback_queue.name,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )
        await exchange.publish(message=message, routing_key=routing_key)

        future = asyncio.Future()

        async def on_response(message: aio_pika.abc.AbstractIncomingMessage):
            async with message.process():
                future.set_result(json.loads(message.body.decode()))

        await callback_queue.consume(on_response)

        return await future
