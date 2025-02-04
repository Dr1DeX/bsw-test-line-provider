from decimal import Decimal

from pydantic import (
    BaseModel,
    Field,
)

from src.status import EventStatus


class BetsBaseSchema(BaseModel):
    event_id: str


class BetsCreateSchema(BetsBaseSchema):
    sum_bet: Decimal = Field(..., gt=0, description="The bet amount must be strictly positive with two decimal places.")


class BetsSchema(BetsBaseSchema):
    status: EventStatus
