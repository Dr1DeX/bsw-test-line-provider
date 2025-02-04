import logging
import uuid
from dataclasses import dataclass
from datetime import datetime

from redis import asyncio as redis

from src.line_provider.schema import (
    EventCreateSchema,
    EventSchema,
    EventUpdateSchema,
)
from src.status import EventStatus


@dataclass
class LineProviderWriteRepository:
    redis_client: redis.Redis

    async def create_event(self, event: EventCreateSchema) -> dict:
        event_id = str(uuid.uuid4())
        event_data = event.dict()
        event_data["event_id"] = event_id
        event_data["coefficient"] = float(event_data["coefficient"])
        event_data["status"] = event_data["status"].value
        await self.redis_client.hset(f"event:{event_id}", mapping=event_data)
        return {"event_id": event_id}

    async def update_event_status(self, new_status: EventUpdateSchema) -> None:
        event_key = f"event:{new_status.event_id}"
        event_data = await self.redis_client.hgetall(event_key)
        event_data = {k.decode(): v.decode() for k, v in event_data.items()}
        if not event_data:
            raise ValueError("Event not found for Redis")
        current_timestamp = int(datetime.now().timestamp())
        if int(event_data["deadline"]) < current_timestamp:
            raise ValueError("Deadline failed")
        await self.redis_client.hset(event_key, "status", new_status.status.value)


@dataclass
class LineProviderReadRepository:
    redis_client: redis.Redis

    async def get_events(self) -> list[EventSchema]:
        valid_events = []
        current_timestamp = int(datetime.now().timestamp())

        async for key in self.redis_client.scan_iter("event:*"):
            event_data = await self.redis_client.hgetall(key)
            logging.info(event_data)
            event_data = {k.decode(): v.decode() for k, v in event_data.items()}
            if not event_data:
                continue
            event_deadline = int(event_data["deadline"])

            if event_deadline < current_timestamp:
                continue
            event_data["event_id"] = str(event_data["event_id"])
            event_data["coefficient"] = float(event_data["coefficient"])
            event_data["status"] = EventStatus(event_data["status"])

            valid_events.append(EventSchema(**event_data))
        return valid_events

    async def get_event(self, event_id: str) -> EventSchema | None:
        event_data = await self.redis_client.hgetall(f"event:{event_id}")
        event_data = {k.decode(): v.decode() for k, v in event_data.items()}
        current_timestamp = int(datetime.now().timestamp())
        if not event_data:
            return None
        if int(event_data["deadline"]) < current_timestamp:
            return None
        event_data["event_id"] = str(event_data["event_id"])
        event_data["coefficient"] = float(event_data["coefficient"])
        event_data["status"] = EventStatus(event_data["status"])
        return EventSchema(**event_data)
