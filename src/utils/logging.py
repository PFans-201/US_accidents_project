"""
Logging configuration for the project.

Provides consistent logging setup across all modules.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from src.config import Config


def setup_logger(
    name: str,
    log_file: Optional[Path] = None,
    level: Optional[str] = None,
    console_output: bool = True
) -> logging.Logger:
    """
    Set up a logger with consistent formatting.
    
    Args:
        name: Logger name (typically __name__ of the calling module)
        log_file: Path to log file. If None, uses Config.LOG_FILE
        level: Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR'). If None, uses Config.LOG_LEVEL
        console_output: Whether to output to console in addition to file
    
    Returns:
        Configured logger instance
    
    Example:
        >>> logger = setup_logger(__name__)
        >>> logger.info("This is an info message")
        >>> logger.warning("This is a warning")
    """
    # Get or create logger
    logger = logging.getLogger(name)
    
    # Set level
    if level is None:
        level = Config.LOG_LEVEL
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(Config.LOG_FORMAT)
    
    # File handler
    if log_file is None:
        log_file = Config.LOG_FILE
    
    log_file = Path(log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, level.upper()))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper()))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # Prevent propagation to avoid duplicate logs
    logger.propagate = False
    
    return logger


def get_module_logger(module_name: str) -> logging.Logger:
    """
    Get logger for a specific module.
    
    Args:
        module_name: Name of the module
    
    Returns:
        Logger instance
    """
    return logging.getLogger(module_name)


if __name__ == "__main__":
    # Test logging
    logger = setup_logger("test_logger")
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    try:
        1 / 0
    except Exception as e:
        logger.exception("Caught an exception:")
