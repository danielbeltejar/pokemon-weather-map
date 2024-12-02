import json
import logging
import sys

from pythonjsonlogger import jsonlogger


class Utf8JsonFormatter(jsonlogger.JsonFormatter):
    def format(self, record):
        log_record = super().format(record)

        log_dict = json.loads(log_record)
        return json.dumps(log_dict, ensure_ascii=False)


def setup_logger(name: str = "app_logger", level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setStream(open(sys.stdout.fileno(), mode='w', encoding='utf-8', closefd=False))

    formatter = Utf8JsonFormatter(
        fmt="%(levelname)s %(asctime)s %(message)s %(name)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    logger.propagate = False

    return logger
