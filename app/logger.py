import logging

from app.config import settings


def setup_logger():
    # Configure the root logger
    logging.basicConfig(
        level=settings.logging.level,
        format=settings.logging.format,
        datefmt=settings.logging.datefmt,
    )
    # Get the root logger
    logger_setup = logging.getLogger()
    return logger_setup


# Call the setup_logger function to create the logger object
logger = setup_logger()
