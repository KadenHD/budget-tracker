import uvicorn

from app.services.config import Config
from app.services.logger import logger

config = Config()


if __name__ == "__main__":
    logger.info(f"Running on {config.URL}")
    if config.IS_DEV:
        logger.warning("Reload is activated")
    logger.info(f"Running in {config.ENV} mode")
    logger.info(f"Logging level: {config.LOG_LEVEL}")

    uvicorn.run(
        "app.app:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.IS_DEV,
        log_config=None
    )
