"""Configuración avanzada de logging estructurado JSON y rotativo."""

import json
import logging
from logging.handlers import RotatingFileHandler
import os


class JSONFormatter(logging.Formatter):
    """Formateador de logs en formato JSON estructurado."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)


def setup_logging() -> logging.Logger:
    """Configura handlers de consola y archivo rotativo."""
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger("secureflow")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = JSONFormatter()

        # Output a consola
        stream_h = logging.StreamHandler()
        stream_h.setFormatter(formatter)
        logger.addHandler(stream_h)

        # Output a archivo rotativo (5MB máximo, 3 copias de respaldo)
        file_h = RotatingFileHandler(
            "logs/app.log", maxBytes=5 * 1024 * 1024, backupCount=3
        )
        file_h.setFormatter(formatter)
        logger.addHandler(file_h)

    return logger