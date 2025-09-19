import uvicorn
import logging
from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.responses import Response

from api.order_book_router import order_book_router

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()],
    force=True
)


def http_exception_handler(_: Request, exc: HTTPException) -> Response:
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(order_book_router, prefix="/api/v1/order-book", tags=["order-book"])
app.add_exception_handler(HTTPException, http_exception_handler)

if __name__ == '__main__':
    uvicorn.run("main:app", port=8080, host="0.0.0.0", reload=True, workers=1)
