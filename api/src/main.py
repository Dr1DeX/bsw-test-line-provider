from fastapi import FastAPI

from src.bet_maker.handlers import router as bet_router


app = FastAPI(title="API Betting Events")

app.include_router(bet_router)
