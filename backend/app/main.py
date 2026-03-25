import uvicorn
from app.services.config import Config
from app.services.logger import logger

config = Config()


if __name__ == "__main__":
    if config.IS_DEV:
        logger.warning(f"Running in {config.ENV} mode (with debug)")

    uvicorn.run(
        "app.app:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.IS_DEV,
        log_config=None
    )
