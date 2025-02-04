import enum

from pydantic import BaseModel


class TestEventStatus(enum.Enum):
    NEW = "NEW"
    FINISHED_WIN = "FINISHED_WIN"
    FINISHED_LOSE = "FINISHED_LOSE"


class TestEventBaseSchema(BaseModel):
    coefficient: float
    deadline: int
    status: TestEventStatus = TestEventStatus.NEW


class TestEventCreateSchema(TestEventBaseSchema):
    pass


class TestEventSchema(TestEventBaseSchema):
    event_id: str


class TestEventUpdateSchema(BaseModel):
    event_id: str
    status: TestEventStatus
