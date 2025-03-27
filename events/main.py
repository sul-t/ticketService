import logging

from fastapi import FastAPI

from src.apps.router import router
from setup_logger import configure_logging


configure_logging()

app = FastAPI()
app.include_router(router)