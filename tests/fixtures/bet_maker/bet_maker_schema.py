import enum

from pydantic import BaseModel


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
