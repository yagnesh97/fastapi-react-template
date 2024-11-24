import secrets
import time
from typing import Any, Callable, TypeVar

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.config import app_description, app_title, app_version, settings
from app.routers.auth import auth
from app.routers.utils import utils
from app.utilities.logger import logger

app = FastAPI(
    title=app_title,
    description=app_description,
    version=app_version,
    docs_url="/",
    root_path=settings.root_path,
)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=[
        "http://localhost:3000",
    ],
)
app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(16))

F = TypeVar("F", bound=Callable[..., Any])


@app.middleware("http")
async def process_time_log_middleware(request: Request, call_next: F) -> Response:
    """
    Add API process time in response headers and log calls
    """
    start_time = time.time()
    response: Response = await call_next(request)
    process_time = str(round(time.time() - start_time, 3))
    response.headers["X-Process-Time"] = process_time

    logger.info(
        "Method=%s Path=%s StatusCode=%s ProcessTime=%s",
        request.method,
        request.url.path,
        response.status_code,
        process_time,
    )
    return response


app.include_router(
    auth.router,
    prefix="/v1/auth",
    tags=["auth"],
)

app.include_router(
    utils.router,
    prefix="/v1/utils",
    tags=["utils"],
)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
