from e3_e4.utils.logging import setup_logging, get_logger

# Test console logging
print("=== Console Logging ===")
setup_logging(log_level="DEBUG", log_format="console")
logger = get_logger("test")
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")

print("\n=== JSON Logging ===")
setup_logging(log_level="INFO", log_format="json")
logger = get_logger("test")
logger.info("JSON formatted message", extra={"user_id": 123, "action": "test"})
