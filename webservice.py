import argparse
import multiprocessing
import os

import uvicorn

from app.core.logging import init_logging

PRODUCTION_PORT: int = 5000
DEVELOPMENT_PORT: int = 8000
HOST: str = "0.0.0.0"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="FastAPI", description="Runs web server for FastAPI")
    parser.add_argument("-r", "--reload", action="store_true", help="")
    parser.add_argument("-p", "--production", action="store_true", help="")
    args = parser.parse_args()

    application_version = next(
        iter({key: value for key, value in os.environ.items() if key.lower() == "application_version"}.values()),
        "Local-Development",
    )
    extra_headers = [("Server", f"FastAPI {application_version}")]

    init_logging("API Initialization")

    uvicorn_arguments = {
        "app": "app.main:app",
        "host": HOST,
        "headers": extra_headers,
        "log_config": None,
        "log_level": None,
    }

    if args.production:
        uvicorn_arguments["workers"] = multiprocessing.cpu_count()
        uvicorn_arguments["port"] = PRODUCTION_PORT
        uvicorn_arguments["proxy_headers"] = True
    else:
        uvicorn_arguments["port"] = DEVELOPMENT_PORT
        if args.reload:
            uvicorn_arguments["reload"] = True

    uvicorn.run(**uvicorn_arguments)
