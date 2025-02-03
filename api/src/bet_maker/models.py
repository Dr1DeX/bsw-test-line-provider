from datetime import datetime

from sqlalchemy import (
    Numeric,
    String,
    TIMESTAMP,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.infrastructure.database import Base


class Events(Base):
    __tablename__ = "Events"

    event_id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    coefficient: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    deadline: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)

    def __repr__(self):
        return f"<Event(id={self.id}, odds={self.odds}, deadline={self.deadline}, status={self.status})>"
