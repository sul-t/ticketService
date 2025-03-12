from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.apps.router import router


app = FastAPI()

app.include_router(router)