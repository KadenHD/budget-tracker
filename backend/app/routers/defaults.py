import psycopg2
from fastapi import APIRouter, status, HTTPException
from app.services.config import Config
from app.services.mailer import get_smtp_async

router = APIRouter(tags=["defaults"])

config = Config()

@router.get(
    "/",
    summary="Get API status",
    status_code=status.HTTP_200_OK,
)
def get_root():
    if config.DEBUG:
        return {"config": config, "status": "ok"}
    return {"status": "ok"}

@router.get(
    "/ping",
    summary="Ping the API",
    status_code=status.HTTP_200_OK,
)
def get_ping():
    return "pong"

@router.get(
    "/health",
    summary="Check system health",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "One or more system components are unhealthy"},
    },
)
async def get_health():
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
