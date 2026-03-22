from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.accounts import Account
from app.models.transactions import Transaction
from app.models.users import User
from app.routers.accounts import get_account
from app.routers.auth import get_current_user
from app.routers.categories import get_category
from app.schemas import MessageResponse
from app.schemas.transactions import (
    TransactionCreate,
    TransactionResponse,
    TransactionUpdate,
)
from app.services.database import get_db

router = APIRouter(
    prefix="/accounts",
    tags=["transactions"],
)

@router.get(
    "/{account_id}/transactions",
    summary="Get the list of account's transactions",
    response_model=list[TransactionResponse],
    status_code=status.HTTP_200_OK,
)
async def get_transactions(
    account_id: str,
    account: Annotated[Account, Depends(get_account)],
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(Transaction).where(Transaction.account_id == account.id))
    transactions = result.scalars().all()
    return transactions

@router.post(
    "/{account_id}/transactions",
    summary="Create a new account's transaction",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(
    account_id: str,
    request: TransactionCreate,
    account: Annotated[Account, Depends(get_account)],
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if request.category_id is not None:
        category = await get_category(account_id, request.category_id, account, user, db)
        category_id = category.id
    else:
        category_id = None

    new_transaction = Transaction(
        amount=request.amount,
        description=request.description,
        date=request.date,
        type=request.type,
        account_id=account.id,
        category_id=category_id,
    )
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    return new_transaction

@router.get(
    "/{account_id}/transactions/{transaction_id}",
    summary="Get a specific account's transaction",
    response_model=TransactionResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Transaction not found"},
    },
)
async def get_transaction(
    account_id: str,
    transaction_id:str,
    account: Annotated[Account, Depends(get_account)],
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(
        select(Transaction).where(
            Transaction.id == transaction_id,
            Transaction.account_id == account.id
        )
    )
    transaction = result.scalars().first()
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return transaction

@router.put(
    "/{account_id}/transactions/{transaction_id}",
    summary="Update a specific account's transaction",
    response_model=TransactionResponse,
)
async def update_transaction(
    account_id: str,
    transaction_id: str,
    request: TransactionUpdate,
    account: Annotated[Account, Depends(get_account)],
    transaction: Annotated[Transaction, Depends(get_transaction)],
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if request.category_id is not None:
        category = await get_category(account_id, request.category_id, account, user, db)
        category_id = category.id
    else:
        category_id = None

    updated = False

    if (request.amount is not None) and (transaction.amount != request.amount):
        transaction.amount = request.amount
        updated = True
    if (request.description is not None) and (transaction.description != request.description):
        transaction.description = request.description
        updated = True
    if (request.date is not None) and (transaction.date != request.date):
        transaction.date = request.date
        updated = True
    if (request.type is not None) and (transaction.type != request.type):
        transaction.type = request.type
        updated = True
    if (category_id is not None) and (transaction.category_id != category_id):
        transaction.category_id = category_id
        updated = True

    if updated:
        await db.commit()
        await db.refresh(transaction)
    return transaction

@router.delete(
    "/{account_id}/transactions/{transaction_id}",
    summary="Delete a specific account's transaction",
    response_model=MessageResponse,
)
async def delete_transaction(
    account_id: str,
    transaction_id: str,
    transaction: Annotated[Transaction, Depends(get_transaction)],
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await db.delete(transaction)
    await db.commit()
    return {"message": "Transaction deleted successfully"}
