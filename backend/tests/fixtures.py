import asyncio
import random

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from tqdm.asyncio import tqdm_asyncio

from app.models.accounts import Account
from app.models.categories import Category
from app.models.transactions import Transaction, TransactionType
from app.models.users import User
from app.services.auth import hash_password
from app.services.database import get_db

fake = Faker()


async def fake_user(db: AsyncSession):
    u = User(
        username=fake.user_name(),
        email=fake.email(),
        password_hash=hash_password("stringst"),
        is_verified=True,
        verification_token=None,
        reset_token=None,
    )
    db.add(u)
    await db.commit()
    await db.refresh(u)
    return u

async def fake_account(db: AsyncSession, user_id: str):
    a = Account(
        name=fake.user_name(),
        user_id=user_id,
    )
    db.add(a)
    await db.commit()
    await db.refresh(a)
    return a

async def fake_category(db: AsyncSession, account_id: str):
    c = Category(
        name=fake.user_name(),
        account_id=account_id,
    )
    db.add(c)
    await db.commit()
    await db.refresh(c)
    return c

async def fake_transaction(db: AsyncSession, account_id: str, category_id: str):
    t = Transaction(
        amount=round(random.uniform(5.0, 5000.0), 2),
        description=fake.sentence(nb_words=6),
        date=fake.date_between(start_date='-1y', end_date='today'), 
        type=random.choice(list(TransactionType)),
        account_id=account_id,
        category_id=category_id,
    )
    db.add(t)
    await db.commit()
    await db.refresh(t)
    return t

async def main():
    n_users = 50
    n_accounts_per_user = 2
    n_categories_per_account = 3
    n_transactions_per_account = 25

    async for db in get_db():
        # User progress bar
        for _ in tqdm_asyncio(range(n_users), desc="Creating users"):
            u = await fake_user(db)
            user_id = u.id

            # Account progress
            for _ in tqdm_asyncio(range(n_accounts_per_user), desc=f"Creating accounts for user {user_id}", leave=False):
                a = await fake_account(db, user_id)
                account_id = a.id

                # Categories progress
                for _ in tqdm_asyncio(range(n_categories_per_account), desc=f"Creating categories for account {account_id}", leave=False):
                    c = await fake_category(db, account_id)
                    category_id = c.id

                # Transactions progress
                for _ in tqdm_asyncio(range(n_transactions_per_account), desc=f"Creating transactions for account {account_id}", leave=False):
                    await fake_transaction(db, account_id, category_id)

        print("\n✅ All fake data created successfully!")

if __name__ == "__main__":
    asyncio.run(main())
