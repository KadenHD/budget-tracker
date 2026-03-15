from fastapi import FastAPI
import uvicorn
from app.config import Config
from app.routers import (
    defaults_router,
    auth_router,
    accounts_router,
    categories_router,
    transactions_router,
    users_router
)

config = Config()

app = FastAPI(
    debug=config.DEBUG,
    title=f"Budget Tracker ({config.ENV})",
    description="A simple and intuitive budget tracker that helps users manage their finances efficiently. Users can create accounts, log transactions, assign categories, and visualize their spending with detailed statistics.",
)

app.include_router(defaults_router)
app.include_router(auth_router)
app.include_router(accounts_router)
app.include_router(categories_router)
app.include_router(transactions_router)
app.include_router(users_router)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )
