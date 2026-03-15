from fastapi import APIRouter

accounts_router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)
