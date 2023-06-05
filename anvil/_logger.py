import logging
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
    },
    "loggers": {
        "anvil": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        }
    },
}


def configure_logging():
    logging.config.dictConfig(LOGGING_CONFIG)


def get_logger(name) -> logging.Logger:
    return logging.getLogger(name)
