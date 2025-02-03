from datetime import datetime

from pydantic import BaseModel


class EventBaseSchema(BaseModel):
    coefficient: float
    deadline: datetime
    status: str


class EventCreateSchema(BaseModel):
    pass


class EventUpdateSchema(BaseModel):
    status: str


class Event(EventBaseSchema):
    event_id: int

    class Config:
        from_attributes = True
