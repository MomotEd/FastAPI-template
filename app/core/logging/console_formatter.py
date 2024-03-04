from loguru._defaults import LOGURU_FORMAT


def format_record(record):
    format_string = str(LOGURU_FORMAT)
    if record["extra"].get("app") is not None:
        format_string += " app: {extra[app]}"
    if record["extra"].get("elapsed_time") is not None:
        format_string += " elapsed_time: {extra[elapsed_time]}"
    format_string += "{exception}\n"
    return format_string
