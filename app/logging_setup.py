import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.config import (
    LOG_BACKUP_COUNT,
    LOG_FILE,
    LOG_MAX_BYTES,
)


def setup_logging(level_name="INFO"):
    logger = logging.getLogger()

    level = getattr(
        logging,
        level_name.upper(),
        logging.INFO,
    )

    logger.setLevel(level)

    if logger.handlers:
        for handler in logger.handlers:
            handler.setLevel(level)

        return logger

    log_path = Path(LOG_FILE)

    handler = RotatingFileHandler(
        log_path,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )

    handler.setFormatter(formatter)
    handler.setLevel(level)

    logger.addHandler(handler)

    return logger
