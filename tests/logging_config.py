import logging
import sys


def setup_logging(
        logger_name: str = None,
        log_level: int = logging.INFO,
        log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        date_format: str = "%Y-%m-%d %H:%M:%S",
) -> logging.Logger:
    """
    Configure a logger with console output and consistent formatting.

    Args:
        logger_name (str): Name of the logger. If None, returns the root logger
        log_level (int): Logging level (default: logging.INFO)
        log_format (str): Format string for log messages
        date_format (str): Format string for timestamp in log messages

    Returns:
        Configured logger instance
    """
    # Get logger instance
    logger = logging.getLogger(logger_name) if logger_name else logging.getLogger()
    logger.setLevel(log_level)

    # Clear any existing handlers
    logger.handlers.clear()

    # Create console handler with formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    # Create formatter
    formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
    console_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(console_handler)

    return logger
