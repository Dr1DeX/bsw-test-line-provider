import uuid
from dataclasses import dataclass

from redis import asyncio as redis

from src.line_provider.schema import (
    EventCreateSchema,
    EventSchema,
    EventUpdateSchema,
)


@dataclass
class LineProviderWriteRepository:
    redis_client: redis.Redis

    async def create_event(self, event: EventCreateSchema) -> dict:
        event_id = str(uuid.uuid4())
        event_data = event.dict()
        event_data["deadline"] = int(event_data["deadline"].timestamp())
        event_data["coefficient"] = float(event_data["coefficient"])
        event_data["status"] = event_data["status"].value
        await self.redis_client.hset(f"event:{event_id}", mapping=event_data)
        return {"event_id": event_id}

    async def update_event_status(self, new_status: EventUpdateSchema) -> None:
        await self.redis_client.hset(f"event:{new_status.event_id}", "status", new_status.status.value)
        ...  # логика проверки валидности эвента и отправка запроса в bet_maker на обновлении статуса


@dataclass
class LineProviderReadRepository:
    redis_client: redis.Redis

    async def get_events(
        self,
    ) -> list[EventSchema]: ...  # нужно слушать события от bet_maker на get_events нужно вернуть все валидные эвенты

    async def get_event(
        self,
    ) -> EventSchema: ...  # нужно слушать события от bet_maker на get_event нужно валидный эвенты
