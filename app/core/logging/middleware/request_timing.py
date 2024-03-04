import time
from contextvars import ContextVar
from typing import Optional

from fastapi import FastAPI
from starlette.datastructures import MutableHeaders
from starlette.types import Scope, Receive, Send, Message

request_time_start_context: ContextVar[Optional[float]] = ContextVar("request_time_start", default=None)


class RequestTimingMiddleware:
    def __init__(self, app: FastAPI, header_name: str = "X-Response-Time", update_request_header: bool = True) -> None:
        self.app = app
        self.header_name = header_name
        self.update_request_header = update_request_header

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] == "http":
            time_before = time.time()
            request_time_start_context.set(time_before)

            async def handle_outgoing_request(message: Message) -> None:
                start_time = request_time_start_context.get()
                if message["type"] == "http.response.start" and start_time is not None:
                    headers = MutableHeaders(scope=message)
                    time_taken = time.time() - start_time
                    headers.append(self.header_name, str(time_taken))
                await send(message)
            await self.app(scope, receive, handle_outgoing_request)
        else:
            await self.app(scope, receive, send)
