"""Custom logging formatters for structured logging.

Implements JSON formatter as specified in ADR-1.0.9 for observability.
"""

import json
import logging
from datetime import UTC, datetime


class JSONFormatter(logging.Formatter):
    """Format log records as JSON lines with request metadata.

    Emits JSON with fields:
    - timestamp: ISO 8601 format with timezone
    - level: Log level name (INFO, WARNING, ERROR, etc.)
    - module: Module name where log originated
    - message: Formatted log message
    - request_id: Request ID from middleware (or '-' if not available)
    - duration_ms: Request duration from middleware (or null if not available)

    The formatter attempts to extract request_id and duration_ms from the
    log record, which are set by RequestIDMiddleware on the request object.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as a JSON line.

        Args:
            record: The log record to format.

        Returns:
            JSON string representing the log entry.
        """
        # Extract request_id from record (set by middleware or custom logging)
        request_id = getattr(record, "request_id", None) or "-"

        # Extract duration_ms from record (set by middleware)
        duration_ms = getattr(record, "duration_ms", None)

        # Build the log entry
        log_entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
            "request_id": request_id,
            "duration_ms": duration_ms,
        }

        # Add exception info if present
        if record.exc_info:
            log_entry["exc_info"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)
