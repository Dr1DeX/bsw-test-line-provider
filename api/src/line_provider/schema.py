import decimal
from datetime import datetime

from pydantic import BaseModel

from src.status import EventStatus


class EventBaseSchema(BaseModel):
    coefficient: decimal.Decimal
    deadline: datetime
    status: EventStatus = EventStatus.NEW


class EventCreateSchema(EventBaseSchema):
    pass


class EventUpdateSchema(BaseModel):
    event_id: str
    status: EventStatus


class EventSchema(EventBaseSchema):
    event_id: int


class EventStatusSchema(BaseModel):
    status: EventStatus
