import sys
from loguru import logger
from pathlib import Path


def create_logger(logger_logfile_path: Path):
    logger.remove()

    logger.add(
        logger_logfile_path,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level="DEBUG",
        rotation="00:00",
        retention="7 days",
        compression="zip",
    )

    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level="DEBUG",
        colorize=True,
    )

    return logger
