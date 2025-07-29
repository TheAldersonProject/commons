# Basic logger

## Purpose

Basic logger is a simple library to be used for logs when only sending logs to the console is
necessary, without any other integration

## Components

Basic logger uses the [Structlog](https://www.structlog.org/) library and emits structured JSON output.

## How to use

### Example 1: *Without LogLevel*

```python
from commons.core import BasicLogger, LogLevel

logger = BasicLogger(log_level=LogLevel.INFO)

logger.debug("I am a debug log message")  # will not be printed in the console
logger.info("I am an info log message")
logger.warning("I am a warning log message")
logger.error("I am an error log message")
logger.critical("I am a critical log message")
```

### Example 2: *Without LogLevel -- assumes DEBUG as default*

```python
from commons.core import BasicLogger, LogLevel

logger = BasicLogger

logger.debug("I am a debug log message")  # will be printed in the console
logger.info("I am an info log message")
logger.warning("I am a warning log message")
logger.error("I am an error log message")
logger.critical("I am a critical log message")
```

## Reference

::: commons.core.basic_logger
