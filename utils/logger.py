"""
Centralized logging setup for the application.
"""

import sys
from loguru import logger
from config import LOGGING_CONFIG

def setup_logger():
    """
    Configure loguru logger with file and console handlers.
    """
    # Remove default handler
    logger.remove()
    
    # Add console handler
    logger.add(
        sys.stdout,
        format=LOGGING_CONFIG["format"],
        level=LOGGING_CONFIG["level"],
    )
    
    # Add file handler
    logger.add(
        str(LOGGING_CONFIG["log_file"]),
        format=LOGGING_CONFIG["format"],
        level=LOGGING_CONFIG["level"],
        rotation="500 MB",
        retention="7 days",
    )
    
    return logger

# Initialize logger
log = setup_logger()