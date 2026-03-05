"""Logging configuration and utilities."""

import logging
import logging.handlers
from pathlib import Path
import os

# Create logs directory if it doesn't exist
LOG_DIR = Path(__file__).parent.parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name (usually __name__)
        level: Logging level
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # File handler
    fh = logging.handlers.RotatingFileHandler(
        LOG_DIR / f"{name.split('.')[-1]}.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    fh.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(fh)
        logger.addHandler(ch)
    
    return logger


# Module-level logger
logger = get_logger(__name__)
