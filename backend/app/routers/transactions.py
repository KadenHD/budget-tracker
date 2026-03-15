from fastapi import APIRouter

transactions_router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)
