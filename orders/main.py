from fastapi import FastAPI

from src.allocation.entrypoints.router import router


app = FastAPI()
app.include_router(router)
