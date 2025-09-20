from fastapi import FastAPI, HTTPException

from app.middleware import include_middleware
from app.routers import include_routers
from main import http_exception_handler


def create_app() -> FastAPI:
    app = FastAPI()
    include_middleware(app)
    include_routers(app)
    app.add_exception_handler(HTTPException, http_exception_handler)
    return app
