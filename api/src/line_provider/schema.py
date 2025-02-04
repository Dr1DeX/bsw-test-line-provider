from pydantic import BaseModel

from src.status import EventStatus


class EventBaseSchema(BaseModel):
    coefficient: float
    deadline: int
    status: EventStatus = EventStatus.NEW


class EventCreateSchema(EventBaseSchema):
    pass


class EventUpdateSchema(BaseModel):
    event_id: str
    status: EventStatus


class EventSchema(EventBaseSchema):
    event_id: str


class EventStatusSchema(BaseModel):
    status: EventStatus
