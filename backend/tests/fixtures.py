import random

from faker import Faker
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from app.services.database import get_db
from app.services.auth import hash_password
from app.models.users import User
from app.models.accounts import Account
from app.models.categories import Category
from app.models.transactions import Transaction, TransactionType

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
        for _ in range(n_users):
            u = await fake_user(db)
            user_id = u.id
            print(f"|--------{user_id}--------|")
            for _ in range(n_accounts_per_user):
                a = await fake_account(db, user_id)
                account_id = a.id

                for _ in range(n_categories_per_account):
                    c = await fake_category(db, account_id)
                    category_id = c.id

                for _ in range(n_transactions_per_account):
                    await fake_transaction(db, account_id, category_id)

            print(f"{n_accounts_per_user} account(s) created")
            print(f"{n_categories_per_account*n_accounts_per_user} categor(y/ies) created")
            print(f"{n_transactions_per_account*n_accounts_per_user} transaction(s) created")

if __name__ == "__main__":
    asyncio.run(main())
