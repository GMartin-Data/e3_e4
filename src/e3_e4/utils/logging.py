"""Logging configuration for CollibrIA."""

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from e3_e4.config import get_settings

# Custom JSON formatter for structured logging


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging (CloudWatch friendly)."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields if present
        extra_fields = {
            k: v
            for k, v in record.__dict__.items()
            if k not in logging.LogRecord.__dict__ and not k.startswith("_")
        }
        if extra_fields:
            log_data["extra"] = extra_fields

        return json.dumps(log_data, ensure_ascii=False)


class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output."""

    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[41m",  # Red background
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        color = self.COLORS.get(record.levelname, "")
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)


def setup_logging(
    log_level: str | None = None,
    log_format: str | None = None,
    log_file: Path | None = None,
) -> None:
    """
    Set up logging configuration.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Format type ('console' or 'json')
        log_file: Optional log file path
    """
    settings = get_settings()
    level = log_level or settings.log_level
    format_type = log_format or settings.log_format

    # Create logs directory if log file is specified
    if log_file and log_file.parent:
        log_file.parent.mkdir(parents=True, exist_ok=True)

    # Clear existing handlers
    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)

    if format_type == "json":
        console_formatter = JSONFormatter()
    else:
        # Console format with colors
        console_format = (
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            if settings.is_production
            else "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
        )
        console_formatter = (
            logging.Formatter(console_format)
            if settings.is_production
            else ColoredFormatter(console_format)
        )

    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # File handler (always JSON for easier parsing)
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(JSONFormatter())
        root_logger.addHandler(file_handler)

    # Set log level
    root_logger.setLevel(level)

    # Adjust third-party loggers
    logging.getLogger("boto3").setLevel(logging.WARNING)
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    # Log startup message
    logger = get_logger(__name__)
    logger.info(
        f"Logging initialized",
        extra={
            "log_level": level,
            "log_format": format_type,
            "environment": settings.environment,
            "log_file": str(log_file) if log_file else None,
        },
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# Convenience functions for structured logging
def log_with_context(
    logger: logging.Logger,
    level: int,
    message: str,
    **context: Any,
) -> None:
    """
    Log a message with additional context.

    Args:
        logger: Logger instance
        level: Log level (e.g., logging.INFO)
        message: Log message
        **context: Additional context to include
    """
    logger.log(level, message, extra=context)


# Initialize logging on module import if running as main application
if __name__ != "__main__":
    # Only auto-initialize in production/when deployed
    if get_settings().environment != "development":
        setup_logging()