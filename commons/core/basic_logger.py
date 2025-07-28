"""Basic logging class for logging in JSON format."""

import logging
import uuid
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

    def __init__(
        self, log_level: LogLevel = LogLevel.DEBUG, logger_uuid: str = None
    ) -> None:
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
            wrapper_class=structlog.make_filtering_bound_logger(log_level.value),
            cache_logger_on_first_use=True,
        )

        self._uuid = str(uuid.uuid4()) if not logger_uuid else logger_uuid
        self._log = structlog.get_logger()

    def _enrich_kwargs(self, kwargs):
        if not kwargs:
            kwargs = {}

        kwargs["uuid"] = self._uuid
        return kwargs

    def info(self, message: str, **kwargs) -> None:
        """Log info."""
        self._log.info(message, **self._enrich_kwargs(kwargs))

    def debug(self, message: str, **kwargs) -> None:
        """Log debug."""
        self._log.debug(message, **self._enrich_kwargs(kwargs))

    def warning(self, message: str, **kwargs) -> None:
        """Log warning."""
        self._log.warning(message, **self._enrich_kwargs(kwargs))

    def error(self, message: str, **kwargs) -> None:
        """Log error."""
        self._log.error(message, **self._enrich_kwargs(kwargs))

    def critical(self, message: str, **kwargs) -> None:
        """Log critical."""
        self._log.critical(message, **self._enrich_kwargs(kwargs))
