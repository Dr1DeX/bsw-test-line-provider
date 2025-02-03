import decimal

from sqlalchemy import (
    Enum,
    Numeric,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.infrastructure.database import Base
from src.status import EventStatus


class Bets(Base):
    __tablename__ = "Bets"

    event_id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    sum_bet: Mapped[decimal.Decimal] = mapped_column(Numeric(100, 2), nullable=False)
    status: Mapped[EventStatus] = mapped_column(Enum(EventStatus), nullable=False)

    def __repr__(self):
        return f"<Bet(id={self.event_id}, status={self.status})>"
