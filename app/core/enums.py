from enum import Enum


class LoggingLevelEnum(Enum):
    INFO = "INFO"
    ERROR = "ERROR"
    WARNING = "WARNING"


class LoggingDestinationEnum(Enum):
    STDOUT_HUMAN_READABLE = "stdout_human_readable"
    STDOUT_JSOM = "stdout_json"
    FLUENT_FORMATTER = "fluent_formatter"
