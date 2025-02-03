import decimal

from pydantic import BaseModel

from src.status import EventStatus


class BetsBaseSchema(BaseModel):
    event_id: int


class BetsCreateSchema(BetsBaseSchema):
    sum_bet: decimal.Decimal


class BetsSchema(BetsBaseSchema):
    status: EventStatus
