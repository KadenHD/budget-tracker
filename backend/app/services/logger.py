import logging
import sys
from pathlib import Path

from loguru import logger

from app.services.config import Config

config = Config()

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

class InterceptHandler(logging.Handler):
    """Redirect standard logging messages to Loguru"""
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

def setup_logger():
    """Configure Loguru to log to console and file"""
    logger.remove()

    logger.add(
        sys.stdout,
        level=config.LOG_LEVEL,
        format="<green>{time:HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
        colorize=True
    )

    logger.add(
        LOG_DIR / "budget_tracker_{time:YYYY-MM-DD}.log",
        level=config.LOG_LEVEL,
        rotation="1 day",
        retention="7 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    )

    for name in logging.root.manager.loggerDict:
        if name in ("uvicorn",):
            uvicorn_logger = logging.getLogger(name)
            uvicorn_logger.handlers.clear()
            uvicorn_logger.setLevel(config.LOG_LEVEL)
            uvicorn_logger.addHandler(InterceptHandler())

    logging.basicConfig(handlers=[InterceptHandler()], level=config.LOG_LEVEL)

setup_logger()
