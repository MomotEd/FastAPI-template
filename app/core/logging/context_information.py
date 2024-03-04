from time import time
from .middleware import request_time_start_context


def add_context_information(record):
    time_started = request_time_start_context.get()
    if time_started is not None:
        record["extra"].update({"elapsed_time": time() - time_started})
