from typing import Optional

from fastapi import APIRouter, Depends, Query

from api.dependencies import get_order_service
from api.order_request import OrderRequest
from application.order_service import OrderService
from domain.order_side import OrderSide

order_book_router = APIRouter()


@order_book_router.get("/health")
def health_check():
    """
    Health check endpoint for container health monitoring.
    """
    return {"status": "healthy", "service": "order-matching"}


@order_book_router.get("/open")
def get_open_orders(
        symbol: Optional[str] = Query(None),
        side: Optional[OrderSide] = Query(None),
        price: Optional[int] = Query(None),
        order_service: OrderService = Depends(get_order_service)
):
    """
    Retrieve all open orders from the order book.
    """
    order_book = order_service.fetch_open_orders(symbol, side, price)
    return order_book.to_dict()


@order_book_router.post("/add")
def add_order(order_request: OrderRequest
              , order_service: OrderService = Depends(get_order_service)
):
    """
    Add a new order to the order book.
    """
    order = order_service.add_order(order_request)
    return order.to_dict()
