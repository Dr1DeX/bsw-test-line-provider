from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from src.bet_maker.schema import (
    BetsBaseSchema,
    BetsCreateSchema,
    BetsSchema,
)
from src.bet_maker.service import BetService
from src.dependency import get_bet_service
from src.line_provider.schema import EventSchema


router = APIRouter(prefix="/api/v1", tags=["bet"])


@router.get("/events", response_model=list[EventSchema])
async def get_events(bet_service: Annotated[BetService, Depends(get_bet_service)]):
    return await bet_service.get_events()


@router.get("/bets", response_model=list[BetsSchema])
async def get_bets(bet_service: Annotated[BetService, Depends(get_bet_service)]):
    return await bet_service.get_bets()


@router.post("/bet", response_model=BetsBaseSchema, status_code=status.HTTP_201_CREATED)
async def create_bet(bet_service: Annotated[BetService, Depends(get_bet_service)], bet: BetsCreateSchema):
    return await bet_service.create_bet(bet=bet)
