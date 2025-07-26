"""Basic logging class for logging in JSON format."""

import logging
from enum import Enum

import structlog


class LogLevel(Enum):
    """Enum for logging levels."""

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class BasicLogger:
    """Basic logging class for logging in JSON format."""

    def __init__(self, log_level: LogLevel = LogLevel.DEBUG) -> None:
        logging.basicConfig(
            format="%(message)s",
            level=log_level.value,
        )

        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.stdlib.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.JSONRenderer(),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
            cache_logger_on_first_use=True,
        )

        self._log = structlog.get_logger()

    def info(self, message: str, **kwargs) -> None:
        """Log info."""
        self._log.info(message, **kwargs)

    def debug(self, message: str, **kwargs) -> None:
        """Log debug."""
        self._log.debug(message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        """Log warning."""
        self._log.warning(message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        """Log error."""
        self._log.error(message, **kwargs)

    def critical(self, message: str, **kwargs) -> None:
        """Log critical."""
        self._log.critical(message, **kwargs)
