from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from redis import asyncio as redis

from src.bet_maker.repository import (
    BetsReadRepository,
    BetsWriteRepository,
)
from src.bet_maker.service import BetService
from src.infrastructure.database.accessor import get_db_session
from src.infrastructure.storage.accessor import get_redis_connection
from src.line_provider.repository import (
    LineProviderReadRepository,
    LineProviderWriteRepository,
)
from src.line_provider.service import LineProviderService


async def get_bet_read_repository(db_session: AsyncSession = Depends(get_db_session)) -> BetsReadRepository:
    return BetsReadRepository(db_session=db_session)


async def get_bet_write_repository(db_session: AsyncSession = Depends(get_db_session)) -> BetsWriteRepository:
    return BetsWriteRepository(db_session=db_session)


async def get_bet_service(
    bet_read_repository: BetsReadRepository = Depends(get_bet_read_repository),
    bet_write_repository: BetsWriteRepository = Depends(get_bet_write_repository),
) -> BetService:
    return BetService(bet_read_repository=bet_read_repository, bet_write_repository=bet_write_repository)


async def get_line_provider_read_repository(
    redis_client: redis.Redis = Depends(get_redis_connection),
) -> LineProviderReadRepository:
    return LineProviderReadRepository(redis_client=redis_client)


async def get_line_provider_write_repository(
    redis_client: redis.Redis = Depends(get_redis_connection),
) -> LineProviderWriteRepository:
    return LineProviderWriteRepository(redis_client=redis_client)


async def get_line_provider_service(
    line_provider_read_repo: LineProviderReadRepository = Depends(get_line_provider_read_repository),
    line_provider_write_repo: LineProviderWriteRepository = Depends(get_line_provider_write_repository),
) -> LineProviderService:
    return LineProviderService(
        line_provider_read_repo=line_provider_read_repo,
        line_provider_write_repo=line_provider_write_repo,
    )
