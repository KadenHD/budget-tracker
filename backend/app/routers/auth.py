from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import MessageResponse
from app.schemas.auth import Settings, Token
from app.schemas.users import UserCreate, UserResponse, UserUpdatePassword
from app.services.auth import (
    EXPIRED,
    create_access_token,
    create_email_verification_token,
    create_reset_token,
    hash_password,
    oauth2_scheme,
    verify_access_token,
    verify_email_verification_token,
    verify_password,
    verify_reset_token,
)
from app.services.config import Config
from app.services.database import get_db
from app.services.mailer import send_mail_async

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

config = Config()
settings = Settings()

@router.post(
    "/register",
    summary="Register a new user",
    response_model=MessageResponse,
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
        password_hash=hash_password(user.password),
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = create_email_verification_token(str(new_user.id))
    new_user.verification_token = hash_password(token)
    await db.commit()
    await db.refresh(new_user)

    verification_url = f"{config.URL}/auth/verify-email?token={token}"
    await send_mail_async(
        sender="your@email.com",
        recipient=new_user.email,
        subject="Verify your email",
        body_html=f"""
        <h3>Verify your email</h3>
        <p>Click the link below:</p>
        <a href="{verification_url}">Verify Email</a>
        """,
    )

    return {"message": "Account created, check your mail to validate your account"}

@router.get(
    "/verify-email",
    summary="Verify email link",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Verification link expired or invalid token or already used token"},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def verify_email(token: str, db: Annotated[AsyncSession, Depends(get_db)],):
    result = verify_email_verification_token(token)

    if result == EXPIRED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification link expired. Please request a new one.",
        )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
        )

    user_id = str(result)

    result_db = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result_db.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not user.verification_token or not verify_password(token, user.verification_token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or already used token",
        )

    user.is_verified = True

    user.verification_token = None

    await db.commit()

    return {"message": "Email successfully verified"}

@router.post(
    "/resend-verification",
    summary="Resend a verification email",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
async def resend_verification(email: str, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(User).where(func.lower(User.email) == email.lower())
    )
    user = result.scalars().first()

    if not user:
        return {"message": "If the email exists, a verification link was sent."}

    if user.is_verified:
        return {"message": "Account already verified"}

    token = create_email_verification_token(str(user.id))

    user.verification_token = hash_password(token)
    await db.commit()
    await db.refresh(user)

    verification_url = f"{config.URL}/auth/verify-email?token={token}"

    await send_mail_async(
        sender="your@email.com",
        recipient=user.email,
        subject="Verify your email",
        body_html=f"""
        <p>Your previous link expired.</p>
        <a href="{verification_url}">Verify Email</a>
        """
    )

    return {"message": "Verification email sent"}

@router.post(
    "/forgot-password",
    summary="Send reset link",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
async def forgot_password(email: str, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(User).where(func.lower(User.email) == email.lower())
    )
    user = result.scalars().first()

    if user:
        token = create_reset_token(str(user.id))

        user.reset_token = hash_password(token)
        await db.commit()
        await db.refresh(user)

        reset_url = f"{config.URL}/auth/reset-password?token={token}"

        await send_mail_async(
            sender="your@email.com",
            recipient=user.email,
            subject="Reset your password",
            body_html=f"""
            <p>Reset your password.</p>
            <a href="{reset_url}">Reset Password</a>
            """
        )

    return {"message": "If the email exists, a reset link was sent"}

@router.post(
    "/reset-password",
    summary="Reset password from link",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Reset link expired or invalid token or already used token"},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def reset_password(token:str, update_user: UserUpdatePassword, db: Annotated[AsyncSession, Depends(get_db)]):
    result = verify_reset_token(token)

    if result == EXPIRED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset link expired. Please request a new one.",
        )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
        )

    user_id = str(result)

    result_db = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result_db.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if not user.reset_token or not verify_password(token, user.reset_token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or already used token",
        )

    user.password_hash = hash_password(update_user.password)

    user.reset_token = None

    await db.commit()
    await db.refresh(user)

    await send_mail_async(
        sender="your@email.com",
        recipient=user.email,
        subject="Password reseted",
        body_html="""
        <p>Password reseted.</p>
        """
    )

    return {"message": "Password successfully reset"}

@router.post(
    "/login",
    summary="Authenticate a user and return a JWT token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials"},
        status.HTTP_403_FORBIDDEN: {"description": "Email not verified"},
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

    if not user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="Email not verified"
        )

    access_token = create_access_token(subject=str(user.id))

    return Token(access_token=access_token, token_type="bearer")

@router.get(
    "/me",
    summary="Get the currently authenticated user",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid or expired token"},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
async def get_me( # NOTE: Can use it as middleware doing 'user: str = Depends(get_me)'
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = verify_access_token(token)

    if result == EXPIRED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token expired, please log in again",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = str(result)

    try:
        # NOTE: Sometime JWT Token change types so we convert "id" back to str (uuid4).
        user_id_str = str(user_id)
    except (TypeError, ValueError) as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from err

    result = await db.execute(
        select(User).where(User.id == user_id_str),
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
