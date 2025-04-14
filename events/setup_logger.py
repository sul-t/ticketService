from enum import StrEnum
import logging


LOG_LEVEL = logging.INFO
LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"


class LogLevels(StrEnum):
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    debug = "DEBUG"

LOG_LEVEL_MAPPING = {
    LogLevels.debug: logging.DEBUG,
    LogLevels.info: logging.INFO,
    LogLevels.warning: logging.WARNING,
    LogLevels.error: logging.ERROR
}

def configure_logging() -> None:
    log_level_name = logging.getLevelName(LOG_LEVEL)

    try:
        log_level = LogLevels(log_level_name)
        numeric_level = LOG_LEVEL_MAPPING[log_level]
    except ValueError:
        numeric_level = logging.ERROR

    if log_level == LogLevels.debug:
        logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)
    else:
        logging.basicConfig(level=numeric_level)

    logging.getLogger("slack_sdk.web.base_client").setLevel(logging.CRITICAL)
