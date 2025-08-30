"""This module contains a pre-customised logger which uses a JSON formatter."""

import logging

from common_py.logger.formatters import JSON_FORMATTER

VALID_LEVELS = [
    logging.NOTSET,
    logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL,
    logging.FATAL,
]
"""Valid logging levels from logging module."""


def get_logger(
    name: str | None = None, level: int = logging.INFO, formatter: logging.Formatter | None = None
) -> logging.Logger:
    """Return a logging.Logger instance which can be pre-configured to log in JSON format.

    Parameters:
        name (str): The name of the logger. Defaults to None.
        level (int): The logging level. Defaults to logging.INFO.
        formatter (logging.Formatter): The logging formatter. Defaults to _JSON_FORMATTER.
    """
    if level not in VALID_LEVELS:
        err_msg = f"get_logger() received an invalid logging level of {level}, must be one of {VALID_LEVELS}"
        raise ValueError(err_msg)

    if formatter is None:
        formatter = logging.Formatter()

    logger = logging.getLogger(name=name) if name else logging.getLogger()
    logger.setLevel(level=level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(fmt=formatter)

    logger.handlers.clear()
    logger.addHandler(console_handler)
    return logger


def get_json_logger(name: str | None = None, level: int = logging.INFO) -> logging.Logger:
    """Convenience method to return a JSON logger for logging to the likes of AWS Cloudwatch.

    Parameters:
        name (str): The name of the logger. Defaults to None.
        level (int): The logging level. Defaults to logging.INFO.
    """
    return get_logger(name=name, level=level, formatter=JSON_FORMATTER)
