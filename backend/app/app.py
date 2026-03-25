from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.services.config import Config
from app.routers import accounts, auth, categories, defaults, transactions

config = Config()

app = FastAPI(
    debug=config.IS_DEV,
    docs_url="/docs" if not config.IS_PROD else None,
    redoc_url="/redoc" if not config.IS_PROD else None,
    openapi_url="/openapi.json" if not config.IS_PROD else None,
    title=f"Budget Tracker {f"({config.ENV})" if not config.IS_PROD else ""}",
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
