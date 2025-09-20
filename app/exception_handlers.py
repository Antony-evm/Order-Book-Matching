from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.responses import Response


def http_exception_handler(_: Request, exc: HTTPException) -> Response:
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )