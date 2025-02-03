from fastapi import FastAPI

from src.bet_maker.handlers import router as bet_router
from src.line_provider.handlers import router as line_provider_router


app = FastAPI(title="API Betting Events")

app.include_router(bet_router)
app.include_router(line_provider_router)
