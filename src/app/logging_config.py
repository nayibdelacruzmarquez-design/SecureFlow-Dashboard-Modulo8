import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name
        }
        return json.dumps(log_obj)

def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger = logging.getLogger("secureflow")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger