from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.services.database import get_db
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth import create_access_token, hash_password, oauth2_scheme, verify_access_token, verify_password
from app.schemas.auth import Settings, Token
from app.schemas.users import UserResponse, UserCreate
from app.models import User

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

settings = Settings()

@router.post(
    "/register",
    summary="Register a new user",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Username already exists or Email already registered"},
    },
)
async def post_register(user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(User).where(func.lower(User.username) == user.username.lower()),
    )
    existing_username = result.scalars().first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    result = await db.execute(
        select(User).where(func.lower(User.email) == user.email.lower()),
    )
    existing_email = result.scalars().first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post(
    "/login",
    summary="Authenticate a user and return a JWT token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials"},
    },
)
async def post_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # NOTE: Query User where either email or username matches the input (case-insensitive).
    result = await db.execute(
        select(User).where(
            or_(
                func.lower(User.email) == form_data.username.lower(),
                func.lower(User.username) == form_data.username.lower()
            )
        )
    )
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")

@router.get(
    "/me",
    summary="Get the currently authenticated user",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid or expired token or user not found"},
    },
)
async def get_me(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # NOTE: Sometime JWT Token change types so we convert "id" back to str (uuid4).
        user_id_str = str(user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    result = await db.execute(
        select(User).where(User.id == user_id_str),
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
