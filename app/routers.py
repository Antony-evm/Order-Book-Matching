from fastapi import FastAPI

from api.order_book_router import order_book_router


def include_routers(app: FastAPI):
    app.include_router(
        order_book_router,
        prefix="/api/v1/order-book",
        tags=["order-book"]
    )
