"""Tests for the BasicLogger class."""

import uuid
from unittest.mock import MagicMock, patch

import pytest

from commons.core.basic_logger import BasicLogger, LogLevel


@pytest.fixture
def mock_structlog():
    """Fixture to mock structlog configuration and logger."""
    with (
        patch("structlog.configure") as mock_configure,
        patch("structlog.get_logger") as mock_get_logger,
    ):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        yield mock_configure, mock_logger


class TestBasicLogger:
    """Test suite for BasicLogger class."""

    def test_init_with_default_parameters(self, mock_structlog):
        """Test initialization with default parameters."""
        mock_configure, _ = mock_structlog

        logger = BasicLogger()

        # Verify basicConfig was called with correct parameters
        assert logger._uuid is not None
        assert len(logger._uuid) > 0

        # Verify structlog.configure was called with correct parameters
        mock_configure.assert_called_once()
        call_args = mock_configure.call_args[1]
        assert call_args["cache_logger_on_first_use"] is True
        assert len(call_args["processors"]) == 5

        # Verify log level is set to DEBUG by default
        # Check that wrapper_class is the result of make_filtering_bound_logger
        assert "wrapper_class" in call_args
        assert callable(call_args["wrapper_class"])

    def test_init_with_custom_log_level(self, mock_structlog):
        """Test initialization with custom log level."""
        mock_configure, _ = mock_structlog

        # Verify log level is set to ERROR
        call_args = mock_configure.call_args[1]
        # Check that wrapper_class is the result of make_filtering_bound_logger
        assert "wrapper_class" in call_args
        assert callable(call_args["wrapper_class"])

    def test_init_with_custom_uuid(self, mock_structlog):
        """Test initialization with custom UUID."""
        _, _ = mock_structlog

        custom_uuid = "test-uuid-123"
        logger = BasicLogger(logger_uuid=custom_uuid)

        assert logger._uuid == custom_uuid

    @patch("uuid.uuid4")
    def test_init_generates_uuid_when_not_provided(self, mock_uuid4, mock_structlog):
        """Test that UUID is generated when not provided."""
        _, _ = mock_structlog

        test_uuid = uuid.UUID("12345678-1234-5678-1234-567812345678")
        mock_uuid4.return_value = test_uuid

        logger = BasicLogger()

        assert logger._uuid == str(test_uuid)
        mock_uuid4.assert_called_once()

    def test_enrich_kwargs_with_empty_kwargs(self, mock_structlog):
        """Test _enrich_kwargs with empty kwargs."""
        _, _ = mock_structlog

        logger = BasicLogger(logger_uuid="test-uuid")
        result = logger._enrich_kwargs({})

        assert result == {"uuid": "test-uuid"}

    def test_enrich_kwargs_with_existing_kwargs(self, mock_structlog):
        """Test _enrich_kwargs with existing kwargs."""
        _, _ = mock_structlog

        logger = BasicLogger(logger_uuid="test-uuid")
        result = logger._enrich_kwargs({"key": "value"})

        assert result == {"key": "value", "uuid": "test-uuid"}

    def test_enrich_kwargs_with_none(self, mock_structlog):
        """Test _enrich_kwargs with None."""
        _, _ = mock_structlog

        logger = BasicLogger(logger_uuid="test-uuid")
        result = logger._enrich_kwargs(None)

        assert result == {"uuid": "test-uuid"}

    def test_info_method(self, mock_structlog):
        """Test info method."""
        _, mock_logger = mock_structlog

        logger = BasicLogger(logger_uuid="test-uuid")
        logger.info("Test info message", extra_field="value")

        mock_logger.info.assert_called_once_with(
            "Test info message", extra_field="value", uuid="test-uuid"
        )

    def test_debug_method(self, mock_structlog):
        """Test debug method."""
        _, mock_logger = mock_structlog

        logger = BasicLogger(logger_uuid="test-uuid")
        logger.debug("Test debug message", extra_field="value")

        mock_logger.debug.assert_called_once_with(
            "Test debug message", extra_field="value", uuid="test-uuid"
        )

    def test_warning_method(self, mock_structlog):
        """Test warning method."""
        _, mock_logger = mock_structlog

        logger = BasicLogger(logger_uuid="test-uuid")
        logger.warning("Test warning message", extra_field="value")

        mock_logger.warning.assert_called_once_with(
            "Test warning message", extra_field="value", uuid="test-uuid"
        )

    def test_error_method(self, mock_structlog):
        """Test error method."""
        _, mock_logger = mock_structlog

        logger = BasicLogger(logger_uuid="test-uuid")
        logger.error("Test error message", extra_field="value")

        mock_logger.error.assert_called_once_with(
            "Test error message", extra_field="value", uuid="test-uuid"
        )

    def test_critical_method(self, mock_structlog):
        """Test critical method."""
        _, mock_logger = mock_structlog

        logger = BasicLogger(logger_uuid="test-uuid")
        logger.critical("Test critical message", extra_field="value")

        mock_logger.critical.assert_called_once_with(
            "Test critical message", extra_field="value", uuid="test-uuid"
        )

    def test_log_methods_without_kwargs(self, mock_structlog):
        """Test all log methods without kwargs."""
        _, mock_logger = mock_structlog

        logger = BasicLogger(logger_uuid="test-uuid")

        # Test all methods without kwargs
        logger.info("Info message")
        logger.debug("Debug message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")

        mock_logger.info.assert_called_once_with("Info message", uuid="test-uuid")
        mock_logger.debug.assert_called_once_with("Debug message", uuid="test-uuid")
        mock_logger.warning.assert_called_once_with("Warning message", uuid="test-uuid")
        mock_logger.error.assert_called_once_with("Error message", uuid="test-uuid")
        mock_logger.critical.assert_called_once_with(
            "Critical message", uuid="test-uuid"
        )

    @patch("logging.basicConfig")
    def test_logging_basicconfig_called(self, mock_basicconfig, mock_structlog):
        """Test that logging.basicConfig is called with correct parameters."""
        _, _ = mock_structlog

        mock_basicconfig.assert_called_once_with(
            format="%(message)s",
            level=LogLevel.INFO.value,
        )

    def test_all_log_levels(self, mock_structlog):
        """Test initialization with all log levels."""
        mock_configure, _ = mock_structlog

        # Test all log levels
        for level in LogLevel:
            call_args = mock_configure.call_args[1]
            # Check that wrapper_class is the result of make_filtering_bound_logger
            assert "wrapper_class" in call_args
            assert callable(call_args["wrapper_class"])
            mock_configure.reset_mock()

    @patch("structlog.processors.JSONRenderer")
    def test_json_renderer_used(self, mock_json_renderer, mock_structlog):
        """Test that JSONRenderer is used in the processors."""
        mock_configure, _ = mock_structlog

        mock_json_renderer.assert_called_once()
        call_args = mock_configure.call_args[1]
        assert mock_json_renderer.return_value in call_args["processors"]