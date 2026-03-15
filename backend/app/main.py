from fastapi import FastAPI
import uvicorn
from app.config import Config
from app.routers import defaults, auth, categories, transactions, users

config = Config()

app = FastAPI(
    debug=config.DEBUG,
    title=f"Budget Tracker ({config.ENV})",
    description="A simple and intuitive budget tracker that helps users manage their finances efficiently. Users can create accounts, log transactions, assign categories, and visualize their spending with detailed statistics.",
)

app.include_router(defaults.router)
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )
