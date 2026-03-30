"""Logging setup for the application."""

import logging
import sys
from pathlib import Path

from florencia.core.config.settings import get_config


def setup_logging(name: str = "florencia") -> logging.Logger:
    """Set up application logging."""
    config = get_config()

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.log_level))

    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, config.log_level))

        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        log_path = Path(config.path_logs)
        if config.path_logs and log_path.exists():
            file_handler = logging.FileHandler(log_path / "florencia.log")
            file_handler.setLevel(getattr(logging, config.log_level))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "florencia") -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
