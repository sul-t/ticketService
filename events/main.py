from fastapi import FastAPI, Request, status, Response
from fastapi.responses import JSONResponse

from setup_logger import configure_logging
from src.apps.router import router


configure_logging()

app = FastAPI()
app.include_router(router)


@app.middleware("http")
async def check_role_user(request: Request, call_next):
    methods_for_verification = ["POST", "PUT", "DELETE"]

    if request.method in methods_for_verification:
        user_role = request.headers.get("X-User-Role")
        if user_role != "admin":
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "Forbidden"}
            )

    return await call_next(request)
