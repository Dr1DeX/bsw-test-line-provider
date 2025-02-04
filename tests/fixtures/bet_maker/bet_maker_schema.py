import enum
from decimal import Decimal

from pydantic import (
    BaseModel,
    Field,
)


class TestEventStatus(enum.Enum):
    NEW = "NEW"
    FINISHED_WIN = "FINISHED_WIN"
    FINISHED_LOSE = "FINISHED_LOSE"


class TestBetsSchema(BaseModel):
    event_id: str
    status: TestEventStatus


class TestEventSchema(BaseModel):
    event_id: str
    coefficient: float
    deadline: int
    status: TestEventStatus = TestEventStatus.NEW


class TestBetCreateSchema(BaseModel):
    event_id: str
    sum_bet: Decimal = Field(..., gt=0)


class TestBetBaseSchema(BaseModel):
    event_id: str
