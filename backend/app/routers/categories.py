from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.accounts import Account
from app.models.categories import Category
from app.models.users import User
from app.routers.accounts import get_account
from app.routers.auth import get_current_user
from app.schemas import MessageResponse
from app.schemas.categories import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.database import get_db

router = APIRouter(
    prefix="/accounts",
    tags=["categories"],
)

@router.get(
    "/{account_id}/categories",
    summary="Get the list of accounts's categories",
    response_model=list[CategoryResponse],
    status_code=status.HTTP_200_OK,
)
async def get_categories(
    account_id: str,
    account: Annotated[Account, Depends(get_account)],
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(Category).where(Category.account_id == account.id))
    categories = result.scalars().all()
    return categories

@router.post(
    "/{account_id}/categories",
    summary="Create a new account's category",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Category name already exists"},
    }
)
async def create_category(
    account_id: str,
    request: CategoryCreate,
    account: Annotated[Account, Depends(get_account)],
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    new_category = Category(
        name=request.name,
        account_id=account.id,
    )
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category

@router.get(
    "/{account_id}/categories/{category_id}",
    summary="Get a specific account's category",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Category not found"},
    },
)
async def get_category(
    account_id: str,
    category_id:str,
    account: Annotated[Account, Depends(get_account)],
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(
        select(Category).where(
            Category.id == category_id,
            Category.account_id == account.id
        )
    )
    category = result.scalars().first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return category

@router.put(
    "/{account_id}/categories/{category_id}",
    summary="Update a specific account's category",
    response_model=CategoryResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Category name already exists"},
    }
)
async def update_category(
    account_id: str,
    transaction_id: str,
    request: CategoryUpdate,
    category: Annotated[Category, Depends(get_category)],
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(
        select(Category).where(Category.account_id == account_id, Category.name == request.name)
    )
    existing_category = result.scalars().first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name already exists"
        )

    if category.name != request.name:
        category.name = request.name
        await db.commit()
        await db.refresh(category)
    return category

@router.delete(
    "/{account_id}/categories/{category_id}",
    summary="Delete a specific account's category",
    response_model=MessageResponse,
)
async def delete_category(
    account_id: str,
    transaction_id: str,
    category: Annotated[Category, Depends(get_category)],
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await db.delete(category)
    await db.commit()
    return {"message": "Transaction deleted successfully"}
