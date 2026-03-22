from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.accounts import Account
from app.models.users import User
from app.routers.auth import get_current_user
from app.schemas import MessageResponse
from app.schemas.accounts import AccountCreate, AccountResponse, AccountUpdate
from app.services.database import get_db

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)

@router.get(
    "/",
    summary="Get the list of user's accounts",
    response_model=list[AccountResponse],
    status_code=status.HTTP_200_OK,
)
async def get_accounts(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(Account).where(Account.user_id == user.id))
    accounts = result.scalars().all()
    return accounts

@router.post(
    "/",
    summary="Create a new user's account",
    response_model=AccountResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Account name already exists"},
    }
)
async def create_account(
    request: AccountCreate,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(
        select(Account).where(Account.user_id == user.id, Account.name == request.name)
    )
    existing_account = result.scalars().first()
    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account name already exists"
        )

    new_account = Account(
        name=request.name,
        user_id=user.id
    )
    db.add(new_account)
    await db.commit()
    await db.refresh(new_account)
    return new_account

@router.get(
    "/{account_id}",
    summary="Get a specific user's account",
    response_model=AccountResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Account not found"},
    },
)
async def get_account(
    account_id: str,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(
        select(Account).where(Account.id == account_id, Account.user_id == user.id)
    )
    account = result.scalars().first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    return account

@router.put(
    "/{account_id}",
    summary="Update a specific user's account",
    response_model=AccountResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Account name already exists"},
    }
)
async def update_account(
    account_id: str,
    request: AccountUpdate,
    account: Annotated[Account, Depends(get_account)],
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(
        select(Account).where(Account.user_id == user.id, Account.name == request.name)
    )
    existing_account = result.scalars().first()
    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account name already exists"
        )

    if account.name != request.name:
        account.name = request.name
        await db.commit()
        await db.refresh(account)
    return account

@router.delete(
    "/{account_id}",
    summary="Delete a specific user's account",
    response_model=MessageResponse,
)
async def delete_account(
    account_id: str,
    account: Annotated[Account, Depends(get_account)],
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):

    await db.delete(account)
    await db.commit()
    return {"message": "Account deleted successfully"}
