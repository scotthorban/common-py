"""Pre-defined formatters for the common logger."""

import logging

JSON_FORMATTER = logging.Formatter(
    fmt='{"time":"%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "message": "%(message)s"}'
)
"""A logging formatter for JSON logging."""
