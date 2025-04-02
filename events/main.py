
from fastapi import FastAPI

from setup_logger import configure_logging
from src.apps.router import router


configure_logging()

app = FastAPI()
app.include_router(router)
