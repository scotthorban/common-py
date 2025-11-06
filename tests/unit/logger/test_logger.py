import logging
from json import loads

import pytest

from common_py.logger import JSON_FORMATTER, get_json_logger, get_logger


class _TestHandler(logging.Handler):
    """A handler used to capture the output of the logger such that it can be tested."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.messages = []

    def handle(self, record: logging.LogRecord) -> None:
        self.messages.append(self.format(record))


class TestLogger:
    """Tests the default logger returned by get_logger()."""

    handler = _TestHandler()
    logger = get_logger(name="test", level=logging.INFO)
    logger.addHandler(handler)
    adapter = logging.LoggerAdapter(logger)

    adapter.info(msg="test message")
    last_message = handler.messages[-1]

    def test_get_logger_raises_on_invalid_level(self) -> None:
        pytest.raises(ValueError, get_logger, name="test", level=-1)

    def test_message_is_logged_as_string(self) -> None:
        assert self.last_message == "test message"


class TestJsonLogger:
    """Tests the JSON logger returned by get_json_logger()."""

    handler = _TestHandler()
    handler.setFormatter(JSON_FORMATTER)
    logger = get_json_logger(name="test", level=logging.INFO)
    logger.addHandler(handler)
    adapter = logging.LoggerAdapter(logger)

    adapter.info(msg="test message")
    last_message = handler.messages[-1]
    log_message_dict = loads(s=last_message)

    def test_message_dict_keys(self) -> None:
        assert list(self.log_message_dict.keys()) == ["time", "level", "name", "message"]

    def test_message_dict_level(self) -> None:
        assert self.log_message_dict["level"] == "INFO"

    def test_message_dict_name(self) -> None:
        assert self.log_message_dict["name"] == "test"

    def test_message_dict_message(self) -> None:
        assert self.log_message_dict["message"] == "test message"
