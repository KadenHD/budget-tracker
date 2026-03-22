import psycopg2
from fastapi import APIRouter, HTTPException, status

from app.schemas import HealthResponse, MessageResponse, StatusResponse
from app.services.config import Config
from app.services.mailer import get_smtp_async

router = APIRouter(tags=["defaults"])

config = Config()

@router.get(
    "/",
    summary="Get API status",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
)
def root():
    return {"status": "ok"}

@router.get(
    "/ping",
    summary="Ping the API",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
def ping():
    return {"message": "pong"}

@router.get(
    "/health",
    summary="Check system health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "One or more system components are unhealthy"},
    },
)
async def health():
    db_status = "ok"
    mail_status = "ok"

    try:
        conn = psycopg2.connect(config.POSTGRES_URL)
        conn.close()
    except Exception:
        db_status = "error"

    try:
        async with get_smtp_async():
            pass
    except Exception:
        mail_status = "error"

    overall_status = "ok" if db_status == "ok" and mail_status == "ok" else "error"

    if overall_status == "error":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": overall_status,
                "database": db_status,
                "mailer": mail_status,
            }
        )

    return {
        "status": overall_status,
        "database": db_status,
        "mailer": mail_status,
    }
