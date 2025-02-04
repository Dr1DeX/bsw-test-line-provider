import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.bet_maker.handlers import router as bet_router
from src.consumer import make_provider_consumer
from src.line_provider.handlers import router as line_provider_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(make_provider_consumer())
    yield


app = FastAPI(title="API Betting Events", lifespan=lifespan)

app.include_router(bet_router)
app.include_router(line_provider_router)
