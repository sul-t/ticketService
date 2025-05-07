from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.allocation.entrypoints.router import router


app = FastAPI()
app.include_router(router)
