from pydantic import BaseModel

from src.status import EventStatus


class BetsBaseSchema(BaseModel):
    event_id: str


class BetsCreateSchema(BetsBaseSchema):
    sum_bet: float


class BetsSchema(BetsBaseSchema):
    status: EventStatus
