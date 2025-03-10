from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from auth.src.apps.router import router


app = FastAPI()


@app.get('/')
def main():
    return RedirectResponse(url='/singin')

app.include_router(router)