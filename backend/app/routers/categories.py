from fastapi import APIRouter

categories_router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)
