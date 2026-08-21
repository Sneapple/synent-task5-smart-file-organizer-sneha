"""
Logging configuration for the Smart File Organizer.
"""

import logging
from pathlib import Path


def setup_logger():
    """
    Configure and return the application logger.

    Returns:
        logging.Logger: Configured logger instance.
    """

    log_directory = Path("logs")
    log_directory.mkdir(exist_ok=True)

    log_file = log_directory / "organizer.log"

    logger = logging.getLogger("smart_file_organizer")
    logger.setLevel(logging.INFO)

    # Avoid adding duplicate handlers if setup_logger() is called again.
    if logger.handlers:
        return logger

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger