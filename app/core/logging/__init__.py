import logging

from fastapi import FastAPI
from loguru import logger
from sys import stdout

from app.core.enums import LoggingDestinationEnum
from app.core.logging.console_formatter import format_record
from app.core.logging.context_information import add_context_information
from app.core.logging.intercept_handler import InterceptHandler
from app.core.logging.middleware.request_timing import RequestTimingMiddleware
from app.core.settings import get_settings


def init_logging(logging_source: str = "API") -> None:
    settings = get_settings()
    logging_level = getattr(logging, settings.logging_level.upper(), "INFO")

    logger.remove()

    match settings.logging_destination:
        case LoggingDestinationEnum.STDOUT_HUMAN_READABLE.value:
            logger.add(
                sink=stdout,
                level=logging_level,
                format=format_record,
                backtrace=True,
                diagnose=True,
                colorize=True
            )
        case LoggingDestinationEnum.STDOUT_JSOM.value:
            logger.add(
                sink=stdout,
                level=logging_level,
                backtrace=True,
                diagnose=True,
                colorize=True
            )
        case LoggingDestinationEnum.FLUENT_FORMATTER.value:
            logging_configs = (settings.fluent_host, settings.fluent_port, settings.logging_fluent_tag)
            if any(map(lambda x: x is None, logging_configs)):
                raise ValueError(f"Fluent logging settings is not specified {logging_configs}")
            logger.add(
                sink=stdout,
                level=logging_level,
                backtrace=True,
                diagnose=True,
                enqueue=True,
                colorize=False
            )
    logger.configure(extra={"source": logging_source})
    logger.configure(patcher=add_context_information)
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


def add_logging(app: FastAPI) -> None:
    app.add_middleware(RequestTimingMiddleware)
