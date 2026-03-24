import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.routers import accounts, auth, categories, defaults, transactions
from app.services.config import Config
from app.services.logger import logger

config = Config()

app = FastAPI(
    debug=config.DEBUG,
    title=f"Budget Tracker ({config.ENV})",
    description="A simple and intuitive budget tracker that helps users manage their finances efficiently. Users can create accounts, log transactions, assign categories, and visualize their spending with detailed statistics.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")

app.include_router(defaults.router)
app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(categories.router)
app.include_router(transactions.router)

if __name__ == "__main__":
    if config.DEBUG:
        logger.warning(f"Running in {config.ENV} (with debug)")

    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_config=None
    )
