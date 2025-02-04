import json
import logging
from dataclasses import dataclass

import aio_pika.abc

from src.line_provider.repository import (
    LineProviderReadRepository,
    LineProviderWriteRepository,
)
from src.line_provider.schema import (
    EventCreateSchema,
    EventUpdateSchema,
)
from src.producer import send_to_queue


@dataclass
class LineProviderService:
    line_provider_write_repo: LineProviderWriteRepository
    line_provider_read_repo: LineProviderReadRepository

    async def create_event(self, event: EventCreateSchema) -> dict:
        return await self.line_provider_write_repo.create_event(event=event)

    async def update_event_status(self, new_status: EventUpdateSchema) -> None:
        await self.line_provider_write_repo.update_event_status(new_status=new_status)
        payload = {"event_id": new_status.event_id, "status": new_status.status.value, "action": "update_event"}
        await send_to_queue(exchange_name="bet_maker_exchange", routing_key="update_event", payload=payload)

    async def handle_rpc_request(self, message: aio_pika.abc.AbstractIncomingMessage):
        async with message.process():
            data = json.loads(message.body.decode())
            logging.info(f"Received line_provider data: {data}")
            action = data.get("action")
            event_id = data.get("event_id")

            if action == "get_event" and event_id:
                event = await self.line_provider_read_repo.get_event(event_id=event_id)
                response_data = {"status": event.status.value if event else None}
            elif action == "get_events":
                events = await self.line_provider_read_repo.get_events()
                response_data = {
                    "events": [
                        {
                            "event_id": e.event_id,
                            "status": e.status.value,
                            "coefficient": e.coefficient,
                            "deadline": e.deadline,
                        }
                        for e in events
                    ],
                }
            else:
                response_data = {"error": "Unknown action"}

            await send_to_queue(exchange_name="bet_maker_exchange", routing_key="events", payload=response_data)
