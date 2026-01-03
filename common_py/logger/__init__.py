"""A common logger with a built-in option for JSON formatting."""

from common_py.logger.formatters import JSON_FORMATTER
from common_py.logger.logger import get_json_logger, get_logger

__all__ = ["JSON_FORMATTER", "get_json_logger", "get_logger"]
