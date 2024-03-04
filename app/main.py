"""Main app module."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import add_logging, init_logging
from app.core.settings import ORIGINS
from app.v1.routers.base import router as base_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_logging()
add_logging(app)
app.include_router(base_router, tags=["Basic Routes"])
