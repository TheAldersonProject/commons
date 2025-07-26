from commons import BasicLogger, LogLevel

logger = BasicLogger(LogLevel.DEBUG)

logger.info("Hello World 1", logger_level=LogLevel.INFO.value)
logger.debug("Hello World 2", logger_level=LogLevel.DEBUG.value)
logger.error("Hello World 3", logger_level=LogLevel.ERROR.value)
logger.critical("Hello World 4", logger_level=LogLevel.CRITICAL.value)

logger.info("Hello World 5", xyz="abc")
logger.info("Hello World 6")
