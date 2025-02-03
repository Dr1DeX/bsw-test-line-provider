from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.bet_maker.repository import (
    BetsReadRepository,
    BetsWriteRepository,
)
from src.bet_maker.service import BetService
from src.infrastructure.database.accessor import get_db_session


async def get_bet_read_repository(db_session: AsyncSession = Depends(get_db_session)) -> BetsReadRepository:
    return BetsReadRepository(db_session=db_session)


async def get_bet_write_repository(db_session: AsyncSession = Depends(get_db_session)) -> BetsWriteRepository:
    return BetsWriteRepository(db_session=db_session)


async def get_bet_service(
    bet_read_repository: BetsReadRepository = Depends(get_bet_read_repository),
    bet_write_repository: BetsWriteRepository = Depends(get_bet_write_repository),
) -> BetService:
    return BetService(bet_read_repository=bet_read_repository, bet_write_repository=bet_write_repository)
