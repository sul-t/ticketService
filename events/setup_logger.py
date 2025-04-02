from enum import StrEnum
import logging


LOG_LEVEL = logging.WARNING
LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"


class LogLevels(StrEnum):
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    debug = "DEBUG"

def configure_logging():
    log_level = str(LOG_LEVEL).upper()
    log_levels = list(LogLevels)

    if log_level not in log_levels:
        logging.basicConfig(level=LogLevels.error)
        return

    if log_level == LogLevels.debug:
        logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)
        return

    logging.basicConfig(level=log_level)

    logging.getLogger("slack_sdk.web.base_client").setLevel(logging.CRITICAL)
