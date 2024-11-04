import logging
import json_log_formatter
from logging.handlers import RotatingFileHandler
import sys
import os

def get_advanced_logger(name, log_file: str | None=None, level=logging.INFO):
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # JSON formatter for structured logging
    formatter = json_log_formatter.JSONFormatter()

    # Console handler with JSON output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Optional file handler with rotation
    if log_file:
        file_handler = RotatingFileHandler(log_file, maxBytes=10**6, backupCount=5)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Avoid duplicate logs
    logger.propagate = False

    # Adding extra context to logs
    logger = _add_contextual_logging(logger)

    return logger

def _add_contextual_logging(logger):
    """
    Decorates the logger to add contextual data like environment info.
    """
    old_info = logger.info
    old_error = logger.error
    old_warning = logger.warning

    # Add context to each log level
    def new_info(msg, *args, **kwargs):
        extra = kwargs.get('extra', {})
        extra.update({'environment': os.getenv('ENV', 'development')})
        kwargs['extra'] = extra
        old_info(msg, *args, **kwargs)

    def new_error(msg, *args, **kwargs):
        extra = kwargs.get('extra', {})
        extra.update({'environment': os.getenv('ENV', 'development')})
        kwargs['extra'] = extra
        old_error(msg, *args, **kwargs)

    def new_warning(msg, *args, **kwargs):
        extra = kwargs.get('extra', {})
        extra.update({'environment': os.getenv('ENV', 'development')})
        kwargs['extra'] = extra
        old_warning(msg, *args, **kwargs)

    logger.info = new_info
    logger.error = new_error
    logger.warning = new_warning

    return logger
